from typing import Optional
from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    photo: Optional[str] = None

class UserRegister(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserRead(UserBase):
    id: int

    class Config:
        orm_mode = True
