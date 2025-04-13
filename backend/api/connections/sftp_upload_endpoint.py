from fastapi import APIRouter, HTTPException, UploadFile, File, Form
import os
import tempfile
from connections.session_manager import session_manager
from connections.all_types_connection.sftp_type.sftp_connection import SFTPConnection

router = APIRouter(prefix="/sftp-upload", tags=["SFTP Upload"])

@router.post("/")
async def upload_file(
    session_id: str = Form(...),
    remote_path: str = Form(...),
    file: UploadFile = File(...)
):
    try:
        connection = session_manager.sessions.get(session_id)
        if not connection:
            raise HTTPException(status_code=404, detail="SFTP сессия не найдена")
        
        if not isinstance(connection, SFTPConnection):
            raise HTTPException(status_code=400, detail="Переданный session_id не соответствует SFTP-сессии")
        
        contents = await file.read()
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(contents)
            temp_filename = tmp_file.name
        
        connection.sftp.put(temp_filename, remote_path)
        
        os.remove(temp_filename)
        return {"msg": "Файл успешно загружен"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
