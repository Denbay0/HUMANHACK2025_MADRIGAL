from pydantic_settings import BaseSettings
from pathlib import Path
import sys

# Определяем базовый каталог проекта (для удобства)
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

class Settings(BaseSettings):
    SECRET_KEY: str = "YOUR_SECRET_KEY_HERE"  # Обязательно замените для продакшена
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        # Опционально: можно задать .env файл и его кодировку
        env_file = BASE_DIR / ".env"
        env_file_encoding = "utf-8"

settings = Settings()
