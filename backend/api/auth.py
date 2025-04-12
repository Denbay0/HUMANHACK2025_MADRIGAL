import re
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, validator
from sqlalchemy.orm import Session

from backend.database.models import User
from backend.database.session import get_db
from backend.security import get_password_hash, verify_password, create_access_token
from backend.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])

USERNAME_PASSWORD_REGEX = re.compile(r"^[a-zA-Z0-9_]{4,15}$")

class UserRegister(BaseModel):
    username: str
    password: str

    @validator("username")
    def validate_username(cls, v):
        if not USERNAME_PASSWORD_REGEX.fullmatch(v):
            raise ValueError(
                "Username must be 4 to 15 characters long and contain only letters, digits, or underscore (_)."
            )
        return v

    @validator("password")
    def validate_password(cls, v):
        if not USERNAME_PASSWORD_REGEX.fullmatch(v):
            raise ValueError(
                "Password must be 4 to 15 characters long and contain only letters, digits, or underscore (_)."
            )
        return v

class UserLogin(BaseModel):
    username: str
    password: str

@router.post("/register")
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )

    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        username=user_data.username,
        password_hash=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg": "User registered successfully", "user_id": new_user.id}

@router.post("/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_data.username).first()
    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id
    }
