from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

class RdpConnectionRequest(BaseModel):
    hostname: str
    port: int = 3389
    username: str = None
    password: str = None

router = APIRouter(prefix="/rdp-connection", tags=["RDP Connection"])

@router.post("/", summary="Создание RDP-подключения через Guacamole")
def create_rdp_connection(req: RdpConnectionRequest):
    try:
        from backend.connections.all_types_connection.rdp_type.rdp_connection import RDPConnection
        connection = RDPConnection(req.hostname, req.port, req.username, req.password)
        connection.connect()
        return {"join_url": connection.join_url, "connection_data": connection.connection_data}
    except Exception as e:
        logger.exception("Ошибка при создании RDP-подключения")
        raise HTTPException(status_code=500, detail=str(e))
