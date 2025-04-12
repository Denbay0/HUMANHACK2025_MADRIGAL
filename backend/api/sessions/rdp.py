from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional, List

from backend.database.session_servers import get_servers_db
from backend.database.models_servers import RDPServer
from backend.database.session import get_db as get_users_db
from backend.security import get_user_from_token, decode_access_token
from backend.database.models import User

router_rdp = APIRouter(prefix="/rdp", tags=["RDP"])

class RDPCreate(BaseModel):
    jwt_token: str = Field(..., example="Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
    server_name: str = Field(..., example="My RDP Server")
    host: str = Field(..., example="192.168.0.103")
    port: int = Field(3389, example=3389)
    username: str = Field(..., example="Administrator")
    password: Optional[str] = Field(None, example="secret")
    domain: Optional[str] = Field(None, example="MYDOMAIN")

class RDPUpdate(BaseModel):
    jwt_token: str = Field(..., example="Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
    server_name: Optional[str] = None
    host: Optional[str] = None
    port: Optional[int] = None
    username: Optional[str] = None
    password: Optional[str] = None
    domain: Optional[str] = None

@router_rdp.post("/", response_model=dict)
def create_rdp_server(
    data: RDPCreate,
    db_servers: Session = Depends(get_servers_db),
    user_db: Session = Depends(get_users_db)
):
    current_user = get_user_from_token(data.jwt_token, user_db)
    new_rdp = RDPServer(
        owner_id=current_user.id,
        server_name=data.server_name,
        host=data.host,
        port=data.port,
        username=data.username,
        password=data.password,
        domain=data.domain
    )
    db_servers.add(new_rdp)
    db_servers.commit()
    db_servers.refresh(new_rdp)
    return {"msg": "RDP server created", "id": new_rdp.id}

@router_rdp.get("/", response_model=List[dict])
def get_all_rdp_servers(
    jwt_token: str = Query(..., example="Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."),
    db_servers: Session = Depends(get_servers_db),
    user_db: Session = Depends(get_users_db)
):
    current_user = get_user_from_token(jwt_token, user_db)
    servers = db_servers.query(RDPServer).filter(RDPServer.owner_id == current_user.id).all()
    return [
        {
            "id": s.id,
            "owner_id": s.owner_id,
            "server_name": s.server_name,
            "host": s.host,
            "port": s.port,
            "username": s.username,
            "password": s.password,
            "domain": s.domain
        }
        for s in servers
    ]

@router_rdp.get("/{rdp_id}", response_model=dict)
def get_rdp_server_by_id(
    rdp_id: int,
    jwt_token: str = Query(..., example="Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."),
    db_servers: Session = Depends(get_servers_db),
    user_db: Session = Depends(get_users_db)
):
    current_user = get_user_from_token(jwt_token, user_db)
    rdp_server = db_servers.query(RDPServer).filter(RDPServer.id == rdp_id).first()
    if not rdp_server:
        raise HTTPException(status_code=404, detail="RDP server not found")
    if rdp_server.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You have no permission to view this server")
    return {
        "id": rdp_server.id,
        "owner_id": rdp_server.owner_id,
        "server_name": rdp_server.server_name,
        "host": rdp_server.host,
        "port": rdp_server.port,
        "username": rdp_server.username,
        "password": rdp_server.password,
        "domain": rdp_server.domain
    }

@router_rdp.put("/{rdp_id}", response_model=dict)
def update_rdp_server(
    rdp_id: int,
    data: RDPUpdate,
    db_servers: Session = Depends(get_servers_db),
    user_db: Session = Depends(get_users_db)
):
    current_user = get_user_from_token(data.jwt_token, user_db)
    rdp_server = db_servers.query(RDPServer).filter(RDPServer.id == rdp_id).first()
    if not rdp_server:
        raise HTTPException(status_code=404, detail="RDP server not found")
    if rdp_server.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You have no permission to update this server")
    update_data = data.dict(exclude_unset=True)
    update_data.pop("jwt_token", None)
    for field, value in update_data.items():
        setattr(rdp_server, field, value)
    db_servers.commit()
    db_servers.refresh(rdp_server)
    return {"msg": "RDP server updated", "id": rdp_server.id}

@router_rdp.delete("/{rdp_id}", response_model=dict)
def delete_rdp_server(
    rdp_id: int,
    jwt_token: str = Query(..., example="Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."),
    db_servers: Session = Depends(get_servers_db),
    user_db: Session = Depends(get_users_db)
):
    current_user = get_user_from_token(jwt_token, user_db)
    rdp_server = db_servers.query(RDPServer).filter(RDPServer.id == rdp_id).first()
    if not rdp_server:
        raise HTTPException(status_code=404, detail="RDP server not found")
    if rdp_server.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You have no permission to delete this server")
    db_servers.delete(rdp_server)
    db_servers.commit()
    return {"msg": "RDP server deleted", "id": rdp_id}
