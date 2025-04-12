import config 
import logging
import getpass
from connections.session_manager import SessionManager

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    manager = SessionManager()
    
    print("Выберите тип подключения: ")
    print("1. SSH")
    print("2. FTP")
    print("3. SFTP")
    choice = input("Введите номер (1/2/3): ").strip()
    if choice == "1":
        conn_type = "ssh"
    elif choice == "2":
        conn_type = "ftp"
    elif choice == "3":
        conn_type = "sftp"
    else:
        print("Неверный выбор")
        return

    hostname = input("Введите адрес сервера: ")
    port_str = input("Введите порт (по умолчанию): ")
    if port_str.strip():
        port = int(port_str)
    else:
        # По умолчанию SSH и SFTP: 22, FTP: 21
        port = 22 if conn_type in ["ssh", "sftp"] else 21

    username = input("Введите логин: ")
    password = getpass.getpass("Введите пароль: ")

    try:
        session_id = manager.create_session(conn_type, hostname, port, username, password)
        print(f"Сессия создана с ID: {session_id}")
    except Exception as e:
        print(f"Ошибка при создании сессии: {e}")
        return

    print("Введите команду для выполнения (например, для FTP: LIST; для SFTP: ls /):")
    print("Введите 'exit' для завершения работы с сессией.")
    while True:
        command = input("Команда: ")
        if command.strip().lower() == "exit":
            break
        try:
            stdout, stderr = manager.execute_command(session_id, command)
            print("=== STDOUT ===")
            print(stdout)
            if stderr:
                print("=== STDERR ===")
                print(stderr)
        except Exception as e:
            print(f"Ошибка выполнения команды: {e}")
    
    try:
        manager.close_session(session_id)
        print("Сессия закрыта.")
    except Exception as e:
        print(f"Ошибка при закрытии сессии: {e}")

if __name__ == "__main__":
    main()
