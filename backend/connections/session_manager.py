import uuid

# Импортируем классы из ваших модулей
from connections.all_types_connection.ssh_type.ssh_connection import SSHConnection
from connections.all_types_connection.ftp_type.ftp_connection import FTPConnection
from connections.all_types_connection.sftp_type.sftp_connection import SFTPConnection
# from connections.all_types_connection.rdp_type.rdp_connection import RDPConnection

class SessionManager:
    """
    Менеджер сессий, создающий разные подключения по типу.
    """
    def __init__(self):
        self.sessions = {}

    def create_session(self, conn_type, hostname, port=22, username=None, password=None, key_filename=None, timeout=10):
        session_id = str(uuid.uuid4())
        
        connection_class = None
        if conn_type.lower() == 'ssh':
            connection_class = SSHConnection
        elif conn_type.lower() == 'ftp':
            connection_class = FTPConnection
        elif conn_type.lower() == 'sftp':
            connection_class = SFTPConnection
        # elif conn_type.lower() == 'rdp':
        #     connection_class = RDPConnection
        else:
            raise Exception(f"Неподдерживаемый тип подключения: {conn_type}")

        connection = connection_class(hostname, port, username, password, key_filename, timeout)
        connection.connect()

        self.sessions[session_id] = connection
        return session_id

    def execute_command(self, session_id, command):
        if session_id not in self.sessions:
            raise Exception("Сессия не найдена")
        connection = self.sessions[session_id]
        return connection.execute_command(command)

    def close_session(self, session_id):
        if session_id in self.sessions:
            self.sessions[session_id].close()
            del self.sessions[session_id]
        else:
            raise Exception("Сессия не найдена")
