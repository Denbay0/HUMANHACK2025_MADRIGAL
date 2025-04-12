import os
import httpx
import logging

logger = logging.getLogger(__name__)

class RDPConnection:
    """
    Класс для создания RDP-подключения через Guacamole.
    При вызове connect() происходит авторизация в Guacamole,
    проверка на существование подключения с именем RDP_{hostname},
    создание нового подключения при отсутствии и формирование join_url.
    """
    def __init__(self, hostname, port, username=None, password=None, timeout=10):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.timeout = timeout
        self.join_url = None
        self.connection_data = None

        self.GUACAMOLE_URL = os.getenv("GUACAMOLE_URL", "http://localhost:8080/guacamole")
        self.ADMIN_USERNAME = os.getenv("GUACAMOLE_ADMIN_USERNAME", "guacadmin")
        self.ADMIN_PASSWORD = os.getenv("GUACAMOLE_ADMIN_PASSWORD", "guacadmin")
        self.DATASOURCE = os.getenv("GUACAMOLE_DATASOURCE", "mysql")
        
        self.session = httpx.Client(timeout=self.timeout)

    def get_guacamole_token(self):
        payload = {"username": self.ADMIN_USERNAME, "password": self.ADMIN_PASSWORD}
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        url = f"{self.GUACAMOLE_URL}/api/tokens"
        response = self.session.post(url, data=payload, headers=headers)
        response.raise_for_status()
        token_data = response.json()
        token = token_data.get("authToken")
        if not token:
            raise Exception("Не удалось получить токен авторизации Guacamole")
        return token

    def get_existing_connection(self, token, connection_name):
        url = f"{self.GUACAMOLE_URL}/api/session/data/{self.DATASOURCE}/connections"
        params = {"token": token}
        response = self.session.get(url, params=params)
        response.raise_for_status()
        connections = response.json()
        logger.debug("Список подключений: %s", connections)
        for conn in connections.values():
            if conn.get("name") == connection_name:
                return conn
        return None

    def get_join_url(self, connection_identifier, token):
        """
        Формирует URL для подключения к Guacamole-клиенту.
        Формат: {GUACAMOLE_URL}/#/client/{connection_identifier}?token={token}
        """
        return f"{self.GUACAMOLE_URL}/#/client/{connection_identifier}?token={token}"

    def connect(self):
        token = self.get_guacamole_token()
        connection_name = f"RDP_{self.hostname}"
        existing_conn = self.get_existing_connection(token, connection_name)
        if existing_conn:
            connection_id = existing_conn.get("identifier")
            self.join_url = self.get_join_url(connection_id, token)
            self.connection_data = existing_conn
            logger.info("Подключение с именем '%s' уже существует, id=%s", connection_name, connection_id)
            return

        payload = {
            "name": connection_name,
            "protocol": "rdp",
            "parameters": {
                "hostname": self.hostname,
                "port": str(self.port),
                "ignore-cert": "true",
                "security": "rdp"
            },
            "parentIdentifier": "ROOT",
            "attributes": {}
        }
        if self.username:
            payload["parameters"]["username"] = self.username
        if self.password:
            payload["parameters"]["password"] = self.password

        url = f"{self.GUACAMOLE_URL}/api/session/data/{self.DATASOURCE}/connections"
        params = {"token": token}
        response = self.session.post(url, json=payload, params=params)
        response.raise_for_status()
        created_conn = response.json()
        connection_id = created_conn.get("identifier")
        self.join_url = self.get_join_url(connection_id, token)
        self.connection_data = created_conn
        logger.info("Создано новое RDP-подключение с id=%s", connection_id)

    def close(self):
        self.session.close()

    def execute_command(self, command):
        raise NotImplementedError("execute_command не поддерживается для RDP-соединения")
