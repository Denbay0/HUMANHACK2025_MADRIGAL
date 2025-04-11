import re
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, validator
from sqlalchemy.orm import Session

from backend.database.models import User
from backend.database.session import get_db
from backend.security import get_password_hash

router = APIRouter(prefix="/users", tags=["users"])

# Регулярное выражение для проверки username и пароля (4–15 символов: буквы, цифры, подчеркивание)
USERNAME_PASSWORD_REGEX = re.compile(r"^[a-zA-Z0-9_]{4,15}$")
# Регулярное выражение для проверки номера телефона (опционально с '+' и 7–15 цифр)
PHONE_REGEX = re.compile(r"^\+?[0-9]{7,15}$")


class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    phone: str
    photo: Optional[str] = None

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    username: str
    email: EmailStr
    phone: str
    photo: Optional[str] = None
    password: Optional[str] = None  # поле пароль опциональное при обновлении

    @validator("username")
    def validate_username(cls, v):
        if not USERNAME_PASSWORD_REGEX.fullmatch(v):
            raise ValueError("Username must be 4 to 15 characters long and contain only letters, digits, or underscore (_).")
        return v

    @validator("phone")
    def validate_phone(cls, v):
        if not PHONE_REGEX.fullmatch(v):
            raise ValueError("Phone number format is invalid. Use 7 to 15 digits, optionally starting with '+'.")
        return v

    @validator("password")
    def validate_password(cls, v):
        if v is not None and not USERNAME_PASSWORD_REGEX.fullmatch(v):
            raise ValueError("Password must be 4 to 15 characters long and contain only letters, digits, or underscore (_).")
        return v


@router.get("/", response_model=List[UserRead])
def get_all_users(db: Session = Depends(get_db)):
    """
    Возвращает список всех пользователей.
    """
    users = db.query(User).all()
    return users


@router.get("/{user_id}", response_model=UserRead)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    """
    Возвращает информацию о пользователе по его ID.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserRead)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    """
    Обновляет данные пользователя по его ID.
    Все поля обязательны, но поле password является опциональным. Если пароль передан,
    он будет захеширован перед обновлением.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Проверка на уникальность для username, email и phone, если изменяются
    if user.username != user_update.username:
        if db.query(User).filter(User.username == user_update.username).first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
        user.username = user_update.username

    if user.email != user_update.email:
        if db.query(User).filter(User.email == user_update.email).first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
        user.email = user_update.email

    if user.phone != user_update.phone:
        if db.query(User).filter(User.phone == user_update.phone).first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Phone number already exists")
        user.phone = user_update.phone

    # Обновляем фото (может быть None)
    user.photo = user_update.photo

    # Если пароль передан, обновляем его (хешируя)
    if user_update.password is not None:
        user.password_hash = get_password_hash(user_update.password)

    db.commit()
    db.refresh(user)
    return user
