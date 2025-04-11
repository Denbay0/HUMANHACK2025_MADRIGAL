import logging
import getpass
import config  # Чтобы сразу настроить sys.path
from connections.session_manager import SessionManager

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    manager = SessionManager()

    print("=== Тест SSH-подключения ===")
    hostname = input("Хост (например, 192.168.1.10): ")
    port_str = input("Порт (по умолчанию 22): ")
    port = int(port_str) if port_str else 22
    username = input("Имя пользователя: ")

    auth_choice = input("Аутентификация по (1) паролю или (2) ключу [1/2]: ")
    password = None
    key_filename = None
    if auth_choice == "1":
        password = getpass.getpass("Введите пароль: ")
    elif auth_choice == "2":
        key_filename = input("Путь к приватному ключу: ")
    else:
        print("Неверный выбор аутентификации.")
        return

    try:
        # Создаём SSH-сессию
        session_id = manager.create_session(
            conn_type='ssh',
            hostname=hostname,
            port=port,
            username=username,
            password=password,
            key_filename=key_filename
        )
        print(f"Сессия создана: {session_id}")
    except Exception as e:
        print(f"Ошибка при создании сессии: {e}")
        return

    # Цикл ввода команд
    print("Подключение установлено. Введите команды для выполнения. Для выхода введите 'exit'.\n")

    while True:
        cmd = input("Команда: ")
        if cmd.lower() == "exit":
            print("Завершаем работу...")
            break
        try:
            stdout, stderr = manager.execute_command(session_id, cmd)
            print("=== STDOUT ===")
            print(stdout)
            if stderr.strip():
                print("=== STDERR ===")
                print(stderr)
        except Exception as e:
            print(f"Ошибка при выполнении команды: {e}")

    # Закрываем сессию
    try:
        manager.close_session(session_id)
        print("Сессия закрыта.")
    except Exception as e:
        print(f"Ошибка при закрытии сессии: {e}")

if __name__ == "__main__":
    main()
