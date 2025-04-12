from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Для user.db
from backend.database.session import Base, engine
from backend.database import models  # User

# Для servers.db
from backend.database.session_servers import BaseServers, engineServers
from backend.database import models_servers  # SSHServer, FTPServer, SFTPServer, RDPServer

# Роутеры
from backend.api import auth, user
from backend.api.servers import router_ssh, router_ftp, router_sftp, router_rdp

app = FastAPI(title="MyApp Backend", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Создаём таблицы users в user.db
Base.metadata.create_all(bind=engine)
# Создаём таблицы ssh_servers, ftp_servers, sftp_servers, rdp_servers в servers.db
BaseServers.metadata.create_all(bind=engineServers)

# Подключаем старые роутеры (auth, user) + новые (ssh, ftp, sftp, rdp)
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(router_ssh)
app.include_router(router_ftp)
app.include_router(router_sftp)
app.include_router(router_rdp)

@app.get("/")
def root():
    return {"msg": "Hello, it works!"}
