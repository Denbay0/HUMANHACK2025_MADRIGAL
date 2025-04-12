from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Импорт подключения к базе пользователей (user.db) и моделей (например, User)
from backend.database.session import Base, engine
from backend.database import models  # Модель User и другие

# Импорт подключения к базе серверов (servers.db) и серверных моделей (SSH, FTP, SFTP, RDP)
from backend.database.session_servers import BaseServers, engineServers
from backend.database import models_servers

# Импорт основных роутеров для авторизации и пользователей (остаются в backend/api)
from backend.api import auth, user

# Импорт серверных роутеров, которые теперь находятся в папке backend/api/sesions
from backend.api.sessions import ssh, ftp, sftp, rdp

# Импорт дополнительных эндпоинтов для подключения (если они остались в backend/api/connections)
from backend.api.connections import ssh_connection_endpoint, ftp_connection_endpoint, sftp_connection_endpoint

app = FastAPI(title="MyApp with Users & Servers", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # Для разработки можно оставить "*", для продакшена – укажите разрешённые домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Создание таблиц пользователей в базе user.db
Base.metadata.create_all(bind=engine)
# Создание таблиц серверов в базе servers.db
BaseServers.metadata.create_all(bind=engineServers)

# Подключаем основные роутеры
app.include_router(auth.router)      # /auth: авторизация, регистрация
app.include_router(user.router)      # /users: операции с пользователями

# Подключаем роутеры серверов
app.include_router(ssh.router_ssh)   # /ssh: SSH-серверы
app.include_router(ftp.router_ftp)   # /ftp: FTP-серверы
app.include_router(sftp.router_sftp) # /sftp: SFTP-серверы
app.include_router(rdp.router_rdp)   # /rdp: RDP-серверы

# Подключаем дополнительные эндпоинты подключения
app.include_router(ssh_connection_endpoint.router)
app.include_router(ftp_connection_endpoint.router)
app.include_router(sftp_connection_endpoint.router)

@app.get("/")
def root():
    return {"message": "Welcome to MyApp with Users & Servers"}
