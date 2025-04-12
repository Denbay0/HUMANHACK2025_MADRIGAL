from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database.session import Base, engine
from backend.database import models
from backend.database.session_servers import BaseServers, engineServers
from backend.database import models_servers
from backend.api import auth, user
from backend.api.servers import router_ssh, router_ftp, router_sftp, router_rdp

from backend.api.connections import ssh_connection_endpoint, ftp_connection_endpoint, sftp_connection_endpoint

app = FastAPI(title="MyApp with 2 DBs", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)
models_servers.BaseServers.metadata.create_all(bind=engineServers)

app.include_router(auth.router)      
app.include_router(user.router)      
app.include_router(router_ssh)       
app.include_router(router_ftp)       
app.include_router(router_sftp)      
app.include_router(router_rdp)

app.include_router(ssh_connection_endpoint.router)
app.include_router(ftp_connection_endpoint.router)
app.include_router(sftp_connection_endpoint.router)

@app.get("/")
def root():
    return {"message": "Welcome! Two DB approach: user.db & servers.db."}
