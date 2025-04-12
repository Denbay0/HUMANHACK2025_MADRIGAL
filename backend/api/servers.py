# backend/api/servers.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import List, Optional

from backend.database.session_servers import get_servers_db
from backend.database.models_servers import SSHServer, FTPServer, SFTPServer, RDPServer

# ----------------------------------
# SSH
# ----------------------------------
router_ssh = APIRouter(prefix="/ssh", tags=["SSH"])

class SSHCreate(BaseModel):
    server_name: str = Field(..., example="My SSH Server")
    host: str = Field(..., example="192.168.0.100")
    port: int = Field(22, example=22)
    username: str = Field(..., example="root")
    password: Optional[str] = Field(None, example="secret")
    private_key: Optional[str] = Field(None, example="--BEGIN KEY--...")

class SSHUpdate(BaseModel):
    server_name: Optional[str] = None
    host: Optional[str] = None
    port: Optional[int] = None
    username: Optional[str] = None
    password: Optional[str] = None
    private_key: Optional[str] = None

@router_ssh.post("/", response_model=dict)
def create_ssh_server(data: SSHCreate, db: Session = Depends(get_servers_db)):
    """Создание записи для SSH-сервера."""
    new_ssh = SSHServer(**data.dict())
    db.add(new_ssh)
    db.commit()
    db.refresh(new_ssh)
    return {"msg": "SSH server created", "id": new_ssh.id}

@router_ssh.get("/", response_model=List[dict])
def get_all_ssh_servers(db: Session = Depends(get_servers_db)):
    """Получение списка всех SSH-серверов."""
    servers = db.query(SSHServer).all()
    return [
        {
            "id": s.id,
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
def get_ssh_server_by_id(ssh_id: int, db: Session = Depends(get_servers_db)):
    """Получение одного SSH-сервера по ID."""
    ssh_server = db.query(SSHServer).filter(SSHServer.id == ssh_id).first()
    if not ssh_server:
        raise HTTPException(status_code=404, detail="SSH server not found")
    return {
        "id": ssh_server.id,
        "server_name": ssh_server.server_name,
        "host": ssh_server.host,
        "port": ssh_server.port,
        "username": ssh_server.username,
        "password": ssh_server.password,
        "private_key": ssh_server.private_key
    }

@router_ssh.put("/{ssh_id}", response_model=dict)
def update_ssh_server(ssh_id: int, data: SSHUpdate, db: Session = Depends(get_servers_db)):
    """Обновление полей SSH-сервера по ID."""
    ssh_server = db.query(SSHServer).filter(SSHServer.id == ssh_id).first()
    if not ssh_server:
        raise HTTPException(status_code=404, detail="SSH server not found")

    for field, value in data.dict(exclude_unset=True).items():
        setattr(ssh_server, field, value)

    db.commit()
    db.refresh(ssh_server)
    return {"msg": "SSH server updated", "id": ssh_server.id}


# ----------------------------------
# FTP
# ----------------------------------
router_ftp = APIRouter(prefix="/ftp", tags=["FTP"])

class FTPCreate(BaseModel):
    server_name: str = Field(..., example="My FTP Server")
    host: str = Field(..., example="192.168.0.101")
    port: int = Field(21, example=21)
    username: str = Field(..., example="ftpuser")
    password: Optional[str] = Field(None, example="ftppass")

class FTPUpdate(BaseModel):
    server_name: Optional[str] = None
    host: Optional[str] = None
    port: Optional[int] = None
    username: Optional[str] = None
    password: Optional[str] = None

@router_ftp.post("/", response_model=dict)
def create_ftp_server(data: FTPCreate, db: Session = Depends(get_servers_db)):
    """Создание записи для FTP-сервера."""
    new_ftp = FTPServer(**data.dict())
    db.add(new_ftp)
    db.commit()
    db.refresh(new_ftp)
    return {"msg": "FTP server created", "id": new_ftp.id}

@router_ftp.get("/", response_model=List[dict])
def get_all_ftp_servers(db: Session = Depends(get_servers_db)):
    """Получение списка всех FTP-серверов."""
    servers = db.query(FTPServer).all()
    return [
        {
            "id": s.id,
            "server_name": s.server_name,
            "host": s.host,
            "port": s.port,
            "username": s.username,
            "password": s.password
        }
        for s in servers
    ]

@router_ftp.get("/{ftp_id}", response_model=dict)
def get_ftp_server_by_id(ftp_id: int, db: Session = Depends(get_servers_db)):
    """Получение одного FTP-сервера по ID."""
    ftp_server = db.query(FTPServer).filter(FTPServer.id == ftp_id).first()
    if not ftp_server:
        raise HTTPException(status_code=404, detail="FTP server not found")
    return {
        "id": ftp_server.id,
        "server_name": ftp_server.server_name,
        "host": ftp_server.host,
        "port": ftp_server.port,
        "username": ftp_server.username,
        "password": ftp_server.password
    }

@router_ftp.put("/{ftp_id}", response_model=dict)
def update_ftp_server(ftp_id: int, data: FTPUpdate, db: Session = Depends(get_servers_db)):
    """Обновление полей FTP-сервера по ID."""
    ftp_server = db.query(FTPServer).filter(FTPServer.id == ftp_id).first()
    if not ftp_server:
        raise HTTPException(status_code=404, detail="FTP server not found")

    for field, value in data.dict(exclude_unset=True).items():
        setattr(ftp_server, field, value)

    db.commit()
    db.refresh(ftp_server)
    return {"msg": "FTP server updated", "id": ftp_server.id}


# ----------------------------------
# SFTP
# ----------------------------------
router_sftp = APIRouter(prefix="/sftp", tags=["SFTP"])

class SFTPCreate(BaseModel):
    server_name: str = Field(..., example="My SFTP Server")
    host: str = Field(..., example="192.168.0.102")
    port: int = Field(22, example=22)
    username: str = Field(..., example="sftpuser")
    password: Optional[str] = Field(None, example="sftppass")
    private_key: Optional[str] = Field(None, example="--BEGIN KEY--...")

class SFTPUpdate(BaseModel):
    server_name: Optional[str] = None
    host: Optional[str] = None
    port: Optional[int] = None
    username: Optional[str] = None
    password: Optional[str] = None
    private_key: Optional[str] = None

@router_sftp.post("/", response_model=dict)
def create_sftp_server(data: SFTPCreate, db: Session = Depends(get_servers_db)):
    """Создание записи для SFTP-сервера."""
    new_sftp = SFTPServer(**data.dict())
    db.add(new_sftp)
    db.commit()
    db.refresh(new_sftp)
    return {"msg": "SFTP server created", "id": new_sftp.id}

@router_sftp.get("/", response_model=List[dict])
def get_all_sftp_servers(db: Session = Depends(get_servers_db)):
    """Получение списка всех SFTP-серверов."""
    servers = db.query(SFTPServer).all()
    return [
        {
            "id": s.id,
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
def get_sftp_server_by_id(sftp_id: int, db: Session = Depends(get_servers_db)):
    """Получение одного SFTP-сервера по ID."""
    sftp_server = db.query(SFTPServer).filter(SFTPServer.id == sftp_id).first()
    if not sftp_server:
        raise HTTPException(status_code=404, detail="SFTP server not found")
    return {
        "id": sftp_server.id,
        "server_name": sftp_server.server_name,
        "host": sftp_server.host,
        "port": sftp_server.port,
        "username": sftp_server.username,
        "password": sftp_server.password,
        "private_key": sftp_server.private_key
    }

@router_sftp.put("/{sftp_id}", response_model=dict)
def update_sftp_server(sftp_id: int, data: SFTPUpdate, db: Session = Depends(get_servers_db)):
    """Обновление полей SFTP-сервера по ID."""
    sftp_server = db.query(SFTPServer).filter(SFTPServer.id == sftp_id).first()
    if not sftp_server:
        raise HTTPException(status_code=404, detail="SFTP server not found")

    for field, value in data.dict(exclude_unset=True).items():
        setattr(sftp_server, field, value)

    db.commit()
    db.refresh(sftp_server)
    return {"msg": "SFTP server updated", "id": sftp_server.id}


# ----------------------------------
# RDP
# ----------------------------------
router_rdp = APIRouter(prefix="/rdp", tags=["RDP"])

class RDPCreate(BaseModel):
    server_name: str = Field(..., example="My RDP Server")
    host: str = Field(..., example="192.168.0.103")
    port: int = Field(3389, example=3389)
    username: str = Field(..., example="Administrator")
    password: Optional[str] = Field(None, example="secret")
    domain: Optional[str] = Field(None, example="MYDOMAIN")

class RDPUpdate(BaseModel):
    server_name: Optional[str] = None
    host: Optional[str] = None
    port: Optional[int] = None
    username: Optional[str] = None
    password: Optional[str] = None
    domain: Optional[str] = None

@router_rdp.post("/", response_model=dict)
def create_rdp_server(data: RDPCreate, db: Session = Depends(get_servers_db)):
    """Создание записи для RDP-сервера."""
    new_rdp = RDPServer(**data.dict())
    db.add(new_rdp)
    db.commit()
    db.refresh(new_rdp)
    return {"msg": "RDP server created", "id": new_rdp.id}

@router_rdp.get("/", response_model=List[dict])
def get_all_rdp_servers(db: Session = Depends(get_servers_db)):
    """Получение списка всех RDP-серверов."""
    servers = db.query(RDPServer).all()
    return [
        {
            "id": s.id,
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
def get_rdp_server_by_id(rdp_id: int, db: Session = Depends(get_servers_db)):
    """Получение одного RDP-сервера по ID."""
    rdp_server = db.query(RDPServer).filter(RDPServer.id == rdp_id).first()
    if not rdp_server:
        raise HTTPException(status_code=404, detail="RDP server not found")
    return {
        "id": rdp_server.id,
        "server_name": rdp_server.server_name,
        "host": rdp_server.host,
        "port": rdp_server.port,
        "username": rdp_server.username,
        "password": rdp_server.password,
        "domain": rdp_server.domain
    }

@router_rdp.put("/{rdp_id}", response_model=dict)
def update_rdp_server(rdp_id: int, data: RDPUpdate, db: Session = Depends(get_servers_db)):
    """Обновление полей RDP-сервера по ID."""
    rdp_server = db.query(RDPServer).filter(RDPServer.id == rdp_id).first()
    if not rdp_server:
        raise HTTPException(status_code=404, detail="RDP server not found")

    for field, value in data.dict(exclude_unset=True).items():
        setattr(rdp_server, field, value)

    db.commit()
    db.refresh(rdp_server)
    return {"msg": "RDP server updated", "id": rdp_server.id}
