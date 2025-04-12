from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Подключение к User DB
from backend.database.session import Base, engine
from backend.database import models
# Подключение к Servers DB
from backend.database.session_servers import BaseServers, engineServers
from backend.database import models_servers

# Подключение роутеров
from backend.api import auth, user
from backend.api.servers import router_ssh, router_ftp, router_sftp, router_rdp

app = FastAPI(title="MyApp with 2 DBs", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Создаём таблицы для users (user.db)
models.Base.metadata.create_all(bind=engine)

# Создаём таблицы для servers (servers.db)
models_servers.BaseServers.metadata.create_all(bind=engineServers)

# Подключаем роутеры
app.include_router(auth.router)      # /auth
app.include_router(user.router)      # /users

app.include_router(router_ssh)       # /ssh
app.include_router(router_ftp)       # /ftp
app.include_router(router_sftp)      # /sftp
app.include_router(router_rdp)       # /rdp

@app.get("/")
def root():
    return {"message": "Welcome! Two DB approach: user.db & servers.db."}
