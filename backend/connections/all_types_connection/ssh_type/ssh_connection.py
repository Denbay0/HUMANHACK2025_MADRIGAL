import logging
import paramiko
import threading

from connections.all_types_connection.base.base_connections import BaseConnection

class SSHConnection(BaseConnection):
    def __init__(self, hostname, port=22, username=None, password=None, key_filename=None, timeout=10):
        super().__init__(hostname, port, username, password, key_filename, timeout)
        self.client = None
        self.lock = threading.Lock()

    def connect(self):
        key_file = self.key_filename if self.key_filename and self.key_filename != "string" else None
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.client.connect(
                hostname=self.hostname,
                port=self.port,
                username=self.username,
                password=self.password,
                key_filename=key_file,
                timeout=self.timeout
            )
            logging.info(f"[SSH] Подключение установлено к {self.hostname}:{self.port}")
        except Exception as e:
            logging.error(f"[SSH] Ошибка подключения к {self.hostname}:{self.port} - {e}")
            raise

    def execute_command(self, command):
        if not self.client:
            raise Exception("[SSH] Соединение не установлено – вызовите connect()")
        with self.lock:
            stdin, stdout, stderr = self.client.exec_command(command)
            stdout_data = stdout.read().decode()
            stderr_data = stderr.read().decode()
            return stdout_data, stderr_data

    def open_shell(self):
        """
        Открывает интерактивный shell сессии и возвращает канал.
        Для корректной работы интерактивной сессии (например, vim) используется invoke_shell.
        """
        if not self.client:
            raise Exception("[SSH] Соединение не установлено – вызовите connect()")
        try:
            channel = self.client.invoke_shell(term='xterm')
            logging.info(f"[SSH] Интерактивный shell запущен для {self.hostname}:{self.port}")
            return channel
        except Exception as e:
            logging.error(f"[SSH] Не удалось открыть интерактивный shell: {e}")
            raise

    def close(self):
        if self.client:
            self.client.close()
            logging.info(f"[SSH] Соединение с {self.hostname}:{self.port} закрыто")
