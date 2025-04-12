import logging
import paramiko
from connections.all_types_connection.base.base_connections import BaseConnection

class SFTPConnection(BaseConnection):
    def __init__(self, hostname, port=22, username=None, password=None, key_filename=None, timeout=10):
        # SFTP использует SSH, поэтому порт по умолчанию 22
        super().__init__(hostname, port, username, password, key_filename, timeout)
        self.ssh_client = None
        self.sftp = None

    def connect(self):
        try:
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh_client.connect(
                hostname=self.hostname,
                port=self.port,
                username=self.username,
                password=self.password,
                key_filename=self.key_filename,
                timeout=self.timeout
            )
            self.sftp = self.ssh_client.open_sftp()
            logging.info(f"[SFTP] Подключение установлено к {self.hostname}:{self.port}")
        except Exception as e:
            logging.error(f"[SFTP] Ошибка подключения к {self.hostname}:{self.port} - {e}")
            raise

    def execute_command(self, command):
        """
        Реализуем поддержку команды `ls <path>`.
        Если путь не указан, выводим содержимое текущего каталога ('.').
        """
        parts = command.strip().split(maxsplit=1)
        if not parts:
            raise Exception("[SFTP] Пустая команда")
        if parts[0].lower() == "ls":
            path = parts[1] if len(parts) > 1 else "."
            try:
                files = self.sftp.listdir(path)
                output = "\n".join(files)
                return output, ""
            except Exception as e:
                return "", f"[SFTP] Ошибка выполнения команды ls {path}: {e}"
        else:
            raise Exception(f"[SFTP] Команда '{command}' не поддерживается. Поддерживается: ls <path>.")

    def close(self):
        if self.sftp:
            self.sftp.close()
        if self.ssh_client:
            self.ssh_client.close()
            logging.info(f"[SFTP] Соединение с {self.hostname}:{self.port} закрыто")
