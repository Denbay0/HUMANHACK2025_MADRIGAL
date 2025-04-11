from sqlalchemy import Column, Integer, String
from .session import Base  # импортируем Base из session.py, где он объявлен через declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    photo = Column(String, nullable=True)  # например, URL аватарки или путь к файлу

    def __repr__(self):
        return f"<User(username='{self.username}')>"
