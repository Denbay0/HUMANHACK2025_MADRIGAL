from sqlalchemy import Column, Integer, String
from backend.database.session import Base  # Импортируем Base из session.py

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    photo = Column(String, nullable=True)  # Опционально, для хранения ссылки на фото

    def __repr__(self):
        return f"<User(username='{self.username}')>"
