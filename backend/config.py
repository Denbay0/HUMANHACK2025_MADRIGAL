from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "YOUR_SECRET_KEY_HERE"  # Замените на реальное значение в продакшене
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()
