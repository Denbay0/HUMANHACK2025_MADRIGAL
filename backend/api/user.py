import re
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, validator
from sqlalchemy.orm import Session

from backend.database.models import User
from backend.database.session import get_db
from backend.security import get_password_hash

router = APIRouter(prefix="/users", tags=["users"])

USERNAME_PASSWORD_REGEX = re.compile(r"^[a-zA-Z0-9_]{4,15}$")

class UserRead(BaseModel):
    id: int
    username: str
    photo: Optional[str]

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    """
    Модель для обновления пользователя.
    Можно обновить username, photo,
    а также опционально пароль (password).
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
        # пароль может быть не указан
        if v is not None and not USERNAME_PASSWORD_REGEX.fullmatch(v):
            raise ValueError(
                "Password must be 4 to 15 characters long and contain only letters, digits, or underscore (_)."
            )
        return v

@router.get("/", response_model=List[UserRead])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

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

    # Проверка, не занято ли новое имя другим пользователем
    if user.username != user_data.username:
        if db.query(User).filter(User.username == user_data.username).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists"
            )
        user.username = user_data.username

    # Обновляем photo (может быть None)
    user.photo = user_data.photo

    # Если указан новый пароль - хешируем
    if user_data.password is not None:
        user.password_hash = get_password_hash(user_data.password)

    db.commit()
    db.refresh(user)
    return user
