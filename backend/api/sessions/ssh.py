from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional, List

from backend.database.session_servers import get_servers_db
from backend.database.session import get_db as get_users_db

from backend.database.models_servers import SSHServer
from backend.security import get_user_from_token
from backend.database.models import User

router_ssh = APIRouter(prefix="/ssh", tags=["SSH"])

class SSHCreate(BaseModel):
    jwt_token: str = Field(..., example="Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
    server_name: str = Field(..., example="My SSH Server")
    host: str = Field(..., example="192.168.0.100")
    port: int = Field(22, example=22)
    username: str = Field(..., example="root")
    password: Optional[str] = Field(None, example="secret")
    private_key: Optional[str] = Field(None, example="--BEGIN KEY--...")

class SSHUpdate(BaseModel):
    jwt_token: str = Field(..., example="Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
    server_name: Optional[str] = None
    host: Optional[str] = None
    port: Optional[int] = None
    username: Optional[str] = None
    password: Optional[str] = None
    private_key: Optional[str] = None

@router_ssh.post("/", response_model=dict)
def create_ssh_server(
    data: SSHCreate,
    db_servers: Session = Depends(get_servers_db),
    user_db: Session = Depends(get_users_db)
):
    current_user = get_user_from_token(data.jwt_token, user_db)
    new_ssh = SSHServer(
        owner_id = current_user.id,
        server_name = data.server_name,
        host = data.host,
        port = data.port,
        username = data.username,
        password = data.password,
        private_key = data.private_key
    )
    db_servers.add(new_ssh)
    db_servers.commit()
    db_servers.refresh(new_ssh)
    return {"msg": "SSH server created", "id": new_ssh.id}

@router_ssh.get("/", response_model=List[dict])
def get_all_ssh_servers(
    jwt_token: str = Query(..., example="Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."),
    db_servers: Session = Depends(get_servers_db),
    user_db: Session = Depends(get_users_db)
):
    current_user = get_user_from_token(jwt_token, user_db)
    servers = db_servers.query(SSHServer).filter(SSHServer.owner_id == current_user.id).all()
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

@router_ssh.get("/{ssh_id}", response_model=dict)
def get_ssh_server_by_id(
    ssh_id: int,
    jwt_token: str = Query(..., example="Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."),
    db_servers: Session = Depends(get_servers_db),
    user_db: Session = Depends(get_users_db)
):
    current_user = get_user_from_token(jwt_token, user_db)
    ssh_server = db_servers.query(SSHServer).filter(SSHServer.id == ssh_id).first()
    if not ssh_server:
        raise HTTPException(status_code=404, detail="SSH server not found")
    if ssh_server.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You have no permission to view this server")
    return {
        "id": ssh_server.id,
        "owner_id": ssh_server.owner_id,
        "server_name": ssh_server.server_name,
        "host": ssh_server.host,
        "port": ssh_server.port,
        "username": ssh_server.username,
        "password": ssh_server.password,
        "private_key": ssh_server.private_key
    }

@router_ssh.put("/{ssh_id}", response_model=dict)
def update_ssh_server(
    ssh_id: int,
    data: SSHUpdate,
    db_servers: Session = Depends(get_servers_db),
    user_db: Session = Depends(get_users_db)
):
    current_user = get_user_from_token(data.jwt_token, user_db)
    ssh_server = db_servers.query(SSHServer).filter(SSHServer.id == ssh_id).first()
    if not ssh_server:
        raise HTTPException(status_code=404, detail="SSH server not found")
    if ssh_server.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You have no permission to update this server")
    update_data = data.dict(exclude_unset=True)
    update_data.pop("jwt_token", None)
    for field, value in update_data.items():
        setattr(ssh_server, field, value)
    db_servers.commit()
    db_servers.refresh(ssh_server)
    return {"msg": "SSH server updated", "id": ssh_server.id}

@router_ssh.delete("/{ssh_id}", response_model=dict)
def delete_ssh_server(
    ssh_id: int,
    jwt_token: str = Query(..., example="Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."),
    db_servers: Session = Depends(get_servers_db),
    user_db: Session = Depends(get_users_db)
):
    current_user = get_user_from_token(jwt_token, user_db)
    ssh_server = db_servers.query(SSHServer).filter(SSHServer.id == ssh_id).first()
    if not ssh_server:
        raise HTTPException(status_code=404, detail="SSH server not found")
    if ssh_server.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You have no permission to delete this server")
    db_servers.delete(ssh_server)
    db_servers.commit()
    return {"msg": "SSH server deleted", "id": ssh_id}
