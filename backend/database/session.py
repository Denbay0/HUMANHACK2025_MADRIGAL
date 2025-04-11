from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Путь к файлу SQLite (файл mydatabase.db находится в папке backend)
SQLALCHEMY_DATABASE_URL = "sqlite:///backend/mydatabase.db"

# Параметр check_same_thread=False нужен для работы SQLite в многопоточном режиме
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создаем базовый класс для моделей SQLAlchemy
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
