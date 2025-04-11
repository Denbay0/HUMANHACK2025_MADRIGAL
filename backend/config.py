import sys
from pathlib import Path

from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).resolve().parent

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

PROJECT_MODULE = "connections"

class Settings(BaseSettings):
    SECRET_KEY: str = "YOUR_SECRET_KEY_HERE"   # Обязательно поменяйте для продакшена
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()
