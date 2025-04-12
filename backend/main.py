from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Импорт подключения к базе пользователей
from backend.database.session import Base, engine
from backend.database import models  # Модель User

# Импорт подключения к базе серверов
from backend.database.session_servers import BaseServers, engineServers
from backend.database import models_servers  # Модели для SSH, FTP, SFTP, RDP

# Импорт основных роутеров
from backend.api import auth, user, ssh, ftp, sftp, rdp

# Импорт дополнительных эндпоинтов подключения (например, SSH, FTP, SFTP подключения)
from backend.api.connections import ssh_connection_endpoint, ftp_connection_endpoint, sftp_connection_endpoint

app = FastAPI(title="MyApp with Users & Servers", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Для разработки можно оставить "*", в продакшене лучше задать список разрешенных доменов
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Создаем таблицы в базе пользователей (user.db)
Base.metadata.create_all(bind=engine)
# Создаем таблицы для серверов в базе серверов (servers.db)
BaseServers.metadata.create_all(bind=engineServers)

# Подключаем роутеры
app.include_router(auth.router)             # /auth эндпоинты (авторизация, регистрация)
app.include_router(user.router)             # /users эндпоинты для работы с пользователями
app.include_router(ssh.router_ssh)          # /ssh эндпоинты для SSH-серверов
app.include_router(ftp.router_ftp)          # /ftp эндпоинты для FTP-серверов
app.include_router(sftp.router_sftp)        # /sftp эндпоинты для SFTP-серверов
app.include_router(rdp.router_rdp)          # /rdp эндпоинты для RDP-серверов

# Дополнительные роутеры для подключения
app.include_router(ssh_connection_endpoint.router)
app.include_router(ftp_connection_endpoint.router)
app.include_router(sftp_connection_endpoint.router)

@app.get("/")
def root():
    return {"message": "Welcome to MyApp with Users & Servers"}
