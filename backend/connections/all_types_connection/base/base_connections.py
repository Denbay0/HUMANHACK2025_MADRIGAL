from abc import ABC, abstractmethod

class BaseConnection(ABC):
    """
    Абстрактный базовый класс для любого вида подключения.
    """

    def __init__(self, hostname, port, username, password=None, key_filename=None, timeout=10):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.key_filename = key_filename
        self.timeout = timeout

    @abstractmethod
    def connect(self):
        """Устанавливает соединение с сервером."""
        pass

    @abstractmethod
    def execute_command(self, command):
        """
        Выполняет команду или операцию на сервере
        (для некоторых протоколов может быть заглушкой).
        """
        pass

    @abstractmethod
    def close(self):
        """Закрывает соединение."""
        pass
