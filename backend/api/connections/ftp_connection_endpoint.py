from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from connections.session_manager import session_manager

router = APIRouter(prefix="/connections/ftp", tags=["FTP Connections"])

class FTPConnectionRequest(BaseModel):
    hostname: str
    port: int = 21
    username: str
    password: str
    timeout: int = 10

@router.post("/")
def create_ftp_connection(request: FTPConnectionRequest):
    try:
        session_id = session_manager.create_session(
            conn_type="ftp",
            hostname=request.hostname,
            port=request.port,
            username=request.username,
            password=request.password,
            key_filename=None,
            timeout=request.timeout
        )
        return {"session_id": session_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
