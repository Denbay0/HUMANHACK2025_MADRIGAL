from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional, List

from backend.database.session_servers import get_servers_db
from backend.database.models_servers import SFTPServer
from backend.database.session import get_db as get_users_db
from backend.security import get_user_from_token
from backend.database.models import User

router_sftp = APIRouter(prefix="/sftp", tags=["SFTP"])

class SFTPCreate(BaseModel):
    jwt_token: str = Field(..., example="Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
    server_name: str = Field(..., example="My SFTP Server")
    host: str = Field(..., example="192.168.0.102")
    port: int = Field(22, example=22)
    username: str = Field(..., example="sftpuser")
    password: Optional[str] = Field(None, example="sftppass")
    private_key: Optional[str] = Field(None, example="--BEGIN KEY--...")

class SFTPUpdate(BaseModel):
    jwt_token: str = Field(..., example="Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
    server_name: Optional[str] = None
    host: Optional[str] = None
    port: Optional[int] = None
    username: Optional[str] = None
    password: Optional[str] = None
    private_key: Optional[str] = None

@router_sftp.post("/", response_model=dict)
def create_sftp_server(
    data: SFTPCreate,
    db_servers: Session = Depends(get_servers_db),
    user_db: Session = Depends(get_users_db)
):
    current_user = get_user_from_token(data.jwt_token, user_db)
    new_sftp = SFTPServer(
        owner_id=current_user.id,
        server_name=data.server_name,
        host=data.host,
        port=data.port,
        username=data.username,
        password=data.password,
        private_key=data.private_key
    )
    db_servers.add(new_sftp)
    db_servers.commit()
    db_servers.refresh(new_sftp)
    return {"msg": "SFTP server created", "id": new_sftp.id}

@router_sftp.get("/", response_model=List[dict])
def get_all_sftp_servers(
    jwt_token: str = Query(..., example="Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."),
    db_servers: Session = Depends(get_servers_db),
    user_db: Session = Depends(get_users_db)
):
    current_user = get_user_from_token(jwt_token, user_db)
    servers = db_servers.query(SFTPServer).filter(SFTPServer.owner_id == current_user.id).all()
    return [
        {
            "id": s.id,
            "owner_id": s.owner_id,
            "server_name": s.server_name,
            "host": s.host,
            "port": s.port,
            "username": s.username,
            "password": s.password,
            "private_key": s.private_key
        }
        for s in servers
    ]

@router_sftp.get("/{sftp_id}", response_model=dict)
def get_sftp_server_by_id(
    sftp_id: int,
    jwt_token: str = Query(..., example="Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."),
    db_servers: Session = Depends(get_servers_db),
    user_db: Session = Depends(get_users_db)
):
    current_user = get_user_from_token(jwt_token, user_db)
    sftp_server = db_servers.query(SFTPServer).filter(SFTPServer.id == sftp_id).first()
    if not sftp_server:
        raise HTTPException(status_code=404, detail="SFTP server not found")
    if sftp_server.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You have no permission to view this server")
    return {
        "id": sftp_server.id,
        "owner_id": sftp_server.owner_id,
        "server_name": sftp_server.server_name,
        "host": sftp_server.host,
        "port": sftp_server.port,
        "username": sftp_server.username,
        "password": sftp_server.password,
        "private_key": sftp_server.private_key
    }

@router_sftp.put("/{sftp_id}", response_model=dict)
def update_sftp_server(
    sftp_id: int,
    data: SFTPUpdate,
    db_servers: Session = Depends(get_servers_db),
    user_db: Session = Depends(get_users_db)
):
    current_user = get_user_from_token(data.jwt_token, user_db)
    sftp_server = db_servers.query(SFTPServer).filter(SFTPServer.id == sftp_id).first()
    if not sftp_server:
        raise HTTPException(status_code=404, detail="SFTP server not found")
    if sftp_server.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You have no permission to update this server")
    update_data = data.dict(exclude_unset=True)
    update_data.pop("jwt_token", None)
    for field, value in update_data.items():
        setattr(sftp_server, field, value)
    db_servers.commit()
    db_servers.refresh(sftp_server)
    return {"msg": "SFTP server updated", "id": sftp_server.id}

@router_sftp.delete("/{sftp_id}", response_model=dict)
def delete_sftp_server(
    sftp_id: int,
    jwt_token: str = Query(..., example="Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."),
    db_servers: Session = Depends(get_servers_db),
    user_db: Session = Depends(get_users_db)
):
    current_user = get_user_from_token(jwt_token, user_db)
    sftp_server = db_servers.query(SFTPServer).filter(SFTPServer.id == sftp_id).first()
    if not sftp_server:
        raise HTTPException(status_code=404, detail="SFTP server not found")
    if sftp_server.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You have no permission to delete this server")
    db_servers.delete(sftp_server)
    db_servers.commit()
    return {"msg": "SFTP server deleted", "id": sftp_id}
