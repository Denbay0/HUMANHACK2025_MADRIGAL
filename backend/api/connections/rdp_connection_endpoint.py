from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
import httpx
import logging

from backend.database.session_servers import get_servers_db
from backend.database.models_servers import RDPServer
from backend.database.models import User

router = APIRouter(prefix="/connections/rdp", tags=["RDP Connections"])

class RDPConnectionRequest(BaseModel):
    server_name: str = Field(..., example="My RDP Server")
    hostname: str = Field(..., example="127.0.0.1")
    port: int = Field(3389, example=7777)
    username: str = Field(..., example="User")
    password: str = Field(..., example="password")
    domain: str = Field(None, example="MYDOMAIN")
    timeout: int = Field(10, example=10)

# Настройки для Guacamole API (используем 127.0.0.1)
GUACAMOLE_API_URL = "http://127.0.0.1:8080/guacamole/api"
GUACAMOLE_ADMIN_USER = "guacadmin"
GUACAMOLE_ADMIN_PASS = "guacadmin"
DATA_SOURCE = "mysql"  # Проверьте, что dataSource именно так называется в вашей конфигурации

# Временная заглушка вместо JWT проверки
def dummy_current_user():
    return User(id=1, username="dummy", password_hash="dummy", photo=None)

@router.post("/", response_model=dict)
async def create_rdp_connection(
    request: RDPConnectionRequest,
    db: Session = Depends(get_servers_db),
    current_user: User = Depends(dummy_current_user)
):
    # 1. Сохраняем данные подключения в БД
    rdp_record = RDPServer(
        owner_id=current_user.id,
        server_name=request.server_name,
        host=request.hostname,
        port=request.port,
        username=request.username,
        password=request.password,
        domain=request.domain
    )
    db.add(rdp_record)
    db.commit()
    db.refresh(rdp_record)
    
    # 2. Получаем токен от Guacamole
    async with httpx.AsyncClient() as client:
        token_url = f"{GUACAMOLE_API_URL}/tokens"
        auth_data = {
            "username": GUACAMOLE_ADMIN_USER,
            "password": GUACAMOLE_ADMIN_PASS
        }
        token_resp = await client.post(token_url, data=auth_data)
        if token_resp.status_code != 200:
            raise HTTPException(status_code=500, detail="Ошибка аутентификации Guacamole")
        token_json = token_resp.json()
        token = token_json.get("authToken")
        if not token:
            raise HTTPException(status_code=500, detail="Не удалось получить токен Guacamole")
        
        # 3. Создаём RDP-соединение в Guacamole
        connection_url = f"{GUACAMOLE_API_URL}/session/data/{DATA_SOURCE}/connections"
        connection_payload = {
            "name": request.server_name,
            "protocol": "rdp",
            "parameters": {
                "hostname": request.hostname,
                "port": str(request.port),
                "username": request.username,
                "password": request.password,
                "domain": request.domain if request.domain else ""
            }
        }
        headers = {"Guacamole-Token": token}
        conn_resp = await client.post(connection_url, json=connection_payload, headers=headers)
        if conn_resp.status_code != 200:
            detail = conn_resp.text
            logging.error(f"Guacamole API Error: {detail}")
            raise HTTPException(status_code=500, detail=f"Не удалось создать соединение в Guacamole. Response: {detail}")
        conn_json = conn_resp.json()
        connection_id = conn_json.get("identifier")
        if not connection_id:
            raise HTTPException(status_code=500, detail="Не получен идентификатор соединения Guacamole")
        
        # 4. Формируем URL для подключения клиента
        guac_client_url = f"http://127.0.0.1:8080/guacamole/#/client/{connection_id}?token={token}"
    
    return {
        "guacamole_url": guac_client_url,
        "connection_id": connection_id,
        "rdp_record_id": rdp_record.id
    }
