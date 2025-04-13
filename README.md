![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)
![Go](https://img.shields.io/badge/go-%2300ADD8.svg?style=for-the-badge&logo=go&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

# ServerLink - Центр подключения оболочки и менеджер удалённых файлов

## Описание проекта

ServerLink - это комплексное решение для удалённого управления серверами, объединяющее терминальный доступ, передачу файлов и удалённый рабочий стол в едином веб-интерфейсе.

## Основные возможности

### Терминальный доступ (SSH)
- Полнофункциональный терминал с поддержкой интерактивных приложений (vim, nano)
- Одновременная работа с несколькими сессиями
- Сохранение истории подключений

### Файловый менеджер (SFTP)
- Загрузка и скачивание файлов
- Просмотр и редактирование прав доступа
- Интеграция с SSH-сессиями

### Удалённый рабочий стол (RDP)
- Подключение через Apache Guacamole
- Поддержка Windows/Linux серверов
- Адаптация под разные разрешения экрана

## Технологии

**Фронтенд:**
- React.js
- Xterm.js для терминальных сессий
- WebSocket для передачи данных между сервером и клиентом

**Бэкенд:**
- Python (FastAPI, SQLAlchemy)
- Go (SSH-модуль широкого формата)
- Apache Guacamole (RDP)

**Инфраструктура:**
- Docker контейнеризация
- JWT аутентификация
- Шифрование данных (SHA256)

## Быстрый старт

```bash
    # Клонирование репозитория
    git clone https://github.com/Denbay0/HUMANHACK2025_MADRIGAL.git
    cd HUMANHACK2025_MADRIGAL
```

# Установка зависимостей
```bash
    venv/Scripts/activate
    pip install -r requirements.txt
```

# Запуск Backend части
```bash
    uvicron backend.main:app --reload
```

# Документация будет доступна по адресу
```bash
    http://localhost:8000/docs
```

# Запуск Frontend части
```bash
    cd .\frontend\my-vite-react-app\src\
    npm install
    npm run dev
```

# Веб-приложение будет доступно по адресу
```bash
    http://localhost:5173/
```

# Запуск Apache контейнера (для RDP)
```bash
    cd HUMANHACK2025_MADRIGAL\docker\guacamole
    docker-compose up -d
```

# Apache admin panel доступно по адресу
```bash
    http:///localhost:8080/guacamole/
```