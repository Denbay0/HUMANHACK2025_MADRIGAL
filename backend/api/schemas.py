from typing import Optional
from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    photo: Optional[str] = None  # URL или путь к фото; необязательное поле

class UserRegister(UserBase):
    password: str  # в запросе регистрации передаётся сырой пароль, будет захеширован

class UserLogin(BaseModel):
    username: str
    password: str

class UserRead(UserBase):
    id: int

    class Config:
        orm_mode = True  # поддержка ORM-модели (SQLAlchemy) для автоматического преобразования
