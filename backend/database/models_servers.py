from sqlalchemy import Column, Integer, String, ForeignKey
from backend.database.session_servers import BaseServers

class SSHServer(BaseServers):
    __tablename__ = "ssh_servers"
    id = Column(Integer, primary_key=True, index=True)

    owner_id = Column(Integer, nullable=False)
    server_name = Column(String, nullable=False)
    host = Column(String, nullable=False)
    port = Column(Integer, nullable=False, default=22)
    username = Column(String, nullable=False)
    password = Column(String, nullable=True)
    private_key = Column(String, nullable=True)

class FTPServer(BaseServers):
    __tablename__ = "ftp_servers"
    id = Column(Integer, primary_key=True, index=True)

    owner_id = Column(Integer, nullable=False)
    server_name = Column(String, nullable=False)
    host = Column(String, nullable=False)
    port = Column(Integer, nullable=False, default=21)
    username = Column(String, nullable=False)
    password = Column(String, nullable=True)

class SFTPServer(BaseServers):
    __tablename__ = "sftp_servers"
    id = Column(Integer, primary_key=True, index=True)

    owner_id = Column(Integer, nullable=False)
    server_name = Column(String, nullable=False)
    host = Column(String, nullable=False)
    port = Column(Integer, nullable=False, default=22)
    username = Column(String, nullable=False)
    password = Column(String, nullable=True)
    private_key = Column(String, nullable=True)

class RDPServer(BaseServers):
    __tablename__ = "rdp_servers"
    id = Column(Integer, primary_key=True, index=True)

    owner_id = Column(Integer, nullable=False)
    server_name = Column(String, nullable=False)
    host = Column(String, nullable=False)
    port = Column(Integer, nullable=False, default=3389)
    username = Column(String, nullable=False)
    password = Column(String, nullable=True)
    domain = Column(String, nullable=True)
