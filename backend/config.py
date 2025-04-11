from pydantic_settings import BaseSettings  # Если используете pydantic v2, иначе для v1: from pydantic import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "YOUR_SECRET_KEY_HERE"   # Обязательно поменяйте для продакшена
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()
