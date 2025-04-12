import re
from typing import List, Optional, Dict

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, validator
from sqlalchemy.orm import Session

from backend.database.models import User
from backend.database.session import get_db
from backend.security import get_password_hash, get_current_user
# Если вы добавляете новый эндпоинт, который пробегает по базе серверов, 
# то дополнительно импортируйте нужные зависимости для работы с servers.db:
from backend.database.session_servers import get_servers_db
from backend.database.models_servers import SSHServer, FTPServer, SFTPServer, RDPServer

router = APIRouter(prefix="/users", tags=["users"])

USERNAME_PASSWORD_REGEX = re.compile(r"^[a-zA-Z0-9_]{4,15}$")

class UserRead(BaseModel):
    id: int
    username: str
    photo: Optional[str]  # Если нужно удалить поле фото, уберите и здесь

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    """
    Модель для обновления пользователя.
    Можно обновить username, photo и опционально пароль.
    """
    username: str
    photo: Optional[str] = None
    password: Optional[str] = None

    @validator("username")
    def validate_username(cls, v):
        if not USERNAME_PASSWORD_REGEX.fullmatch(v):
            raise ValueError(
                "Username must be 4 to 15 characters long and contain only letters, digits, or underscore (_)."
            )
        return v

    @validator("password")
    def validate_password(cls, v):
        if v is not None and not USERNAME_PASSWORD_REGEX.fullmatch(v):
            raise ValueError(
                "Password must be 4 to 15 characters long and contain only letters, digits, or underscore (_)."
            )
        return v

@router.get("/", response_model=List[UserRead])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

# Новый эндпоинт для серверов нужно объявить до маршрута "/{user_id}"
@router.get("/servers", response_model=Dict[str, List[dict]])
def get_user_servers(
    current_user: User = Depends(get_current_user),
    db_servers: Session = Depends(get_servers_db)
):
    """
    Возвращает все серверы (SSH, FTP, SFTP, RDP), принадлежащие текущему пользователю.
    """
    ssh_servers = db_servers.query(SSHServer).filter(SSHServer.owner_id == current_user.id).all()
    ftp_servers = db_servers.query(FTPServer).filter(FTPServer.owner_id == current_user.id).all()
    sftp_servers = db_servers.query(SFTPServer).filter(SFTPServer.owner_id == current_user.id).all()
    rdp_servers = db_servers.query(RDPServer).filter(RDPServer.owner_id == current_user.id).all()

    def serialize_server(server) -> dict:
        return {col.name: getattr(server, col.name) for col in server.__table__.columns}

    return {
        "ssh": [serialize_server(s) for s in ssh_servers],
        "ftp": [serialize_server(s) for s in ftp_servers],
        "sftp": [serialize_server(s) for s in sftp_servers],
        "rdp": [serialize_server(s) for s in rdp_servers],
    }

@router.get("/{user_id}", response_model=UserRead)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.put("/{user_id}", response_model=UserRead)
def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if user.username != user_data.username:
        if db.query(User).filter(User.username == user_data.username).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists"
            )
        user.username = user_data.username

    # Если требуется убрать поле photo – можно закомментировать следующую строку:
    user.photo = user_data.photo

    if user_data.password is not None:
        user.password_hash = get_password_hash(user_data.password)

    db.commit()
    db.refresh(user)
    return user
