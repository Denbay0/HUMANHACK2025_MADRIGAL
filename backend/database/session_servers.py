from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_SERVERS_DB_URL = "sqlite:///backend/servers.db"

engineServers = create_engine(
    SQLALCHEMY_SERVERS_DB_URL,
    connect_args={"check_same_thread": False}
)
SessionLocalServers = sessionmaker(autocommit=False, autoflush=False, bind=engineServers)
BaseServers = declarative_base()

def get_servers_db():
    db = SessionLocalServers()
    try:
        yield db
    finally:
        db.close()
