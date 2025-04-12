from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional, List

from backend.database.session_servers import get_servers_db
from backend.database.models_servers import FTPServer
from backend.database.session import get_db as get_users_db
from backend.security import get_user_from_token
from backend.database.models import User

router_ftp = APIRouter(prefix="/ftp", tags=["FTP"])

class FTPCreate(BaseModel):
    jwt_token: str = Field(..., example="Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
    server_name: str = Field(..., example="My FTP Server")
    host: str = Field(..., example="192.168.0.101")
    port: int = Field(21, example=21)
    username: str = Field(..., example="ftpuser")
    password: Optional[str] = Field(None, example="ftppass")

class FTPUpdate(BaseModel):
    jwt_token: str = Field(..., example="Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
    server_name: Optional[str] = None
    host: Optional[str] = None
    port: Optional[int] = None
    username: Optional[str] = None
    password: Optional[str] = None

@router_ftp.post("/", response_model=dict)
def create_ftp_server(
    data: FTPCreate,
    db_servers: Session = Depends(get_servers_db),
    user_db: Session = Depends(get_users_db)
):
    current_user = get_user_from_token(data.jwt_token, user_db)
    new_ftp = FTPServer(
        owner_id=current_user.id,
        server_name=data.server_name,
        host=data.host,
        port=data.port,
        username=data.username,
        password=data.password
    )
    db_servers.add(new_ftp)
    db_servers.commit()
    db_servers.refresh(new_ftp)
    return {"msg": "FTP server created", "id": new_ftp.id}

@router_ftp.get("/", response_model=List[dict])
def get_all_ftp_servers(
    jwt_token: str = Query(..., example="Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."),
    db_servers: Session = Depends(get_servers_db),
    user_db: Session = Depends(get_users_db)
):
    current_user = get_user_from_token(jwt_token, user_db)
    servers = db_servers.query(FTPServer).filter(FTPServer.owner_id == current_user.id).all()
    return [
        {
            "id": s.id,
            "owner_id": s.owner_id,
            "server_name": s.server_name,
            "host": s.host,
            "port": s.port,
            "username": s.username,
            "password": s.password
        }
        for s in servers
    ]

@router_ftp.get("/{ftp_id}", response_model=dict)
def get_ftp_server_by_id(
    ftp_id: int,
    jwt_token: str = Query(..., example="Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."),
    db_servers: Session = Depends(get_servers_db),
    user_db: Session = Depends(get_users_db)
):
    current_user = get_user_from_token(jwt_token, user_db)
    ftp_server = db_servers.query(FTPServer).filter(FTPServer.id == ftp_id).first()
    if not ftp_server:
        raise HTTPException(status_code=404, detail="FTP server not found")
    if ftp_server.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You have no permission to view this server")
    return {
        "id": ftp_server.id,
        "owner_id": ftp_server.owner_id,
        "server_name": ftp_server.server_name,
        "host": ftp_server.host,
        "port": ftp_server.port,
        "username": ftp_server.username,
        "password": ftp_server.password
    }

@router_ftp.put("/{ftp_id}", response_model=dict)
def update_ftp_server(
    ftp_id: int,
    data: FTPUpdate,
    db_servers: Session = Depends(get_servers_db),
    user_db: Session = Depends(get_users_db)
):
    current_user = get_user_from_token(data.jwt_token, user_db)
    ftp_server = db_servers.query(FTPServer).filter(FTPServer.id == ftp_id).first()
    if not ftp_server:
        raise HTTPException(status_code=404, detail="FTP server not found")
    if ftp_server.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You have no permission to update this server")
    update_data = data.dict(exclude_unset=True)
    update_data.pop("jwt_token", None)
    for field, value in update_data.items():
        setattr(ftp_server, field, value)
    db_servers.commit()
    db_servers.refresh(ftp_server)
    return {"msg": "FTP server updated", "id": ftp_server.id}

@router_ftp.delete("/{ftp_id}", response_model=dict)
def delete_ftp_server(
    ftp_id: int,
    jwt_token: str = Query(..., example="Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."),
    db_servers: Session = Depends(get_servers_db),
    user_db: Session = Depends(get_users_db)
):
    current_user = get_user_from_token(jwt_token, user_db)
    ftp_server = db_servers.query(FTPServer).filter(FTPServer.id == ftp_id).first()
    if not ftp_server:
        raise HTTPException(status_code=404, detail="FTP server not found")
    if ftp_server.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You have no permission to delete this server")
    db_servers.delete(ftp_server)
    db_servers.commit()
    return {"msg": "FTP server deleted", "id": ftp_id}
