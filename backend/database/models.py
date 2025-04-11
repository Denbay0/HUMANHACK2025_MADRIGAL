from sqlalchemy import Column, Integer, String
from backend.database.session import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    photo = Column(String, nullable=True)  # Опционально: URL или путь к фото

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}', phone='{self.phone}')>"
