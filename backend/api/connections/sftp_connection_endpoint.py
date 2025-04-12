from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from connections.session_manager import SessionManager

router = APIRouter(prefix="/connections/sftp", tags=["SFTP Connections"])

session_manager = SessionManager()

class SFTPConnectionRequest(BaseModel):
    hostname: str
    port: int = 22
    username: str
    password: str = None
    key_filename: str = None
    timeout: int = 10

@router.post("/")
def create_sftp_connection(request: SFTPConnectionRequest):
    try:
        session_id = session_manager.create_session(
            conn_type="sftp",
            hostname=request.hostname,
            port=request.port,
            username=request.username,
            password=request.password,
            key_filename=request.key_filename,
            timeout=request.timeout
        )
        return {"session_id": session_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
