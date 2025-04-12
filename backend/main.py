from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database.session import Base, engine
from backend.database import models 

from backend.database.session_servers import BaseServers, engineServers
from backend.database import models_servers

from backend.api import auth, user
from backend.api.sessions import ssh, ftp, sftp, rdp
from backend.api.connections import ssh_connection_endpoint, ftp_connection_endpoint, sftp_connection_endpoint

from connections.web_socket.ws_ssh import router as ws_ssh_router

app = FastAPI(title="MyApp with Users & Servers", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
BaseServers.metadata.create_all(bind=engineServers)

app.include_router(auth.router)      
app.include_router(user.router)      
app.include_router(ssh.router_ssh)   
app.include_router(ftp.router_ftp)   
app.include_router(sftp.router_sftp)
app.include_router(rdp.router_rdp)   
app.include_router(ssh_connection_endpoint.router)
app.include_router(ftp_connection_endpoint.router)
app.include_router(sftp_connection_endpoint.router)

app.include_router(ws_ssh_router)

@app.get("/")
def root():
    return {"message": "Welcome to MyApp with Users & Servers"}
