import ftplib
import logging
from connections.all_types_connection.base.base_connections import BaseConnection

class FTPConnection(BaseConnection):
    def __init__(self, hostname, port=21, username=None, password=None, key_filename=None, timeout=10):
        # Для FTP порт по умолчанию 21
        super().__init__(hostname, port, username, password, key_filename, timeout)
        self.ftp = None

    def connect(self):
        try:
            self.ftp = ftplib.FTP()
            self.ftp.connect(self.hostname, self.port, timeout=self.timeout)
            self.ftp.login(self.username, self.password)
            logging.info(f"[FTP] Подключение установлено к {self.hostname}:{self.port}")
        except Exception as e:
            logging.error(f"[FTP] Ошибка подключения к {self.hostname}:{self.port} - {e}")
            raise

    def execute_command(self, command):
        """
        Поддержка ограниченного набора команд для FTP.
        В данном примере реализована команда LIST для получения списка файлов в текущем каталоге.
        """
        if command.strip().upper() == "LIST":
            try:
                files = self.ftp.nlst()
                output = "\n".join(files)
                return output, ""
            except Exception as e:
                return "", f"[FTP] Ошибка выполнения команды LIST: {e}"
        else:
            raise Exception(f"[FTP] Команда '{command}' не поддерживается. Поддерживается только команда LIST.")

    def close(self):
        if self.ftp:
            try:
                self.ftp.quit()
                logging.info(f"[FTP] Соединение с {self.hostname}:{self.port} закрыто")
            except Exception as e:
                logging.error(f"[FTP] Ошибка при закрытии соединения: {e}")
