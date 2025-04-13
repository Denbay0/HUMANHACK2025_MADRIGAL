import logging
import paramiko
import threading

from connections.all_types_connection.base.base_connections import BaseConnection

class SFTPConnection(BaseConnection):
    def __init__(self, hostname, port=22, username=None, password=None, key_filename=None, timeout=10):
        super().__init__(hostname, port, username, password, key_filename, timeout)
        self.transport = None
        self.sftp = None
        self.lock = threading.Lock()

    def connect(self):
        key_file = self.key_filename if self.key_filename and self.key_filename != "string" else None
        
        try:
            self.transport = paramiko.Transport((self.hostname, self.port))
            if key_file:
                pkey = paramiko.RSAKey.from_private_key_file(key_file)
                self.transport.connect(username=self.username, pkey=pkey)
            else:
                self.transport.connect(username=self.username, password=self.password)
            self.sftp = paramiko.SFTPClient.from_transport(self.transport)
            logging.info(f"[SFTP] Подключение установлено к {self.hostname}:{self.port}")
        except Exception as e:
            logging.error(f"[SFTP] Ошибка подключения к {self.hostname}:{self.port} - {e}")
            raise

    def close(self):
        if self.sftp:
            self.sftp.close()
        if self.transport:
            self.transport.close()
        logging.info(f"[SFTP] Соединение с {self.hostname}:{self.port} закрыто")
    
    def execute_command(self, command):
        return "SFTP: выполнение команд не поддерживается"
