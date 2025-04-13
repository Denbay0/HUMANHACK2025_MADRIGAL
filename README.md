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

## Документация будет доступна по адресу
```bash
    http://localhost:8000/docs
```

# Запуск Frontend части
```bash
    cd .\frontend\my-vite-react-app\src\
    npm install
    npm run dev
```

## Веб-приложение будет доступно по адресу
```bash
    http://localhost:5173/
```

# Запуск Apache контейнера (для RDP)
```bash
    cd HUMANHACK2025_MADRIGAL\docker\guacamole
    docker-compose up -d
```
## Apache admin panel доступно по адресу
```bash
    http:///localhost:8080/guacamole/
```


## 🐟 Команда разработчиков

<table>
  <tr>
    <td align="center" style="border: 1px solid #555;">
      <img src="defay_1x9/pics_readme/alexander.jpg" width="100" height="100" style="border-radius: 50%" alt="avatar"><br />
      <b>Александр Штеренфельд</b><br />
      <sub><i>Рандомный чел</i></sub>
      <hr style="border: 1px solid #555; margin: 10px 0;">
      <div align="left">
      <b>Вклад в проект:</b><br />
      • Backend/Frontend разработка<br />
      • Работа с базами данных<br />
      • Работа с подключениями к серверам
      <hr style="border: 1px solid #555; margin: 10px 0;">
      <b>Контакты:</b><br />
      <a href="https://github.com/BeesKnigh">GitHub</a> • <a href="https://t.me/BeesKnights">Telegram</a>
      </div>
    </td>
    <td align="center" style="border: 1px solid #555;">
      <img src="defay_1x9/pics_readme/dafay1x9.jpg" width="100" height="100" style="border-radius: 50%" alt="avatar"><br />
      <b>Денис Байрамов</b><br />
      <sub><i>Backend разработчик</i></sub>
      <hr style="border: 1px solid #555; margin: 10px 0;">
      <div align="left">
      <b>Вклад в проект:</b><br />
      • Backend разработка<br />
      • Работа с базами данных<br />
      <hr style="border: 1px solid #555; margin: 10px 0;">
      <b>Контакты:</b><br />
      <a href="https://github.com/Denbay0">GitHub</a> • <a href="https://t.me/Denbay0">Telegram</a>
      </div>
    </td>
    <td align="center" style="border: 1px solid #555;">
      <img src="defay_1x9/pics_readme/Lera.jpg" width="100" height="100" style="border-radius: 50%" alt="avatar"><br />
      <b>Валерия Якименко</b><br />
      <sub><i>Frontend разработчик</i></sub>
      <hr style="border: 1px solid #555; margin: 10px 0;">
      <div align="left">
      <b>Вклад в проект:</b><br />
      • Reac, Vite разработка<br />
      • Концепт-арты<br />
      • UI/UX дизайн
      <hr style="border: 1px solid #555; margin: 10px 0;">
      <b>Контакты:</b><br />
      <a href="https://github.com/Unkno394">GitHub</a> • <a href="https://t.me/Unkno394">Telegram</a>
      </div>
    </td>
    <td align="center" style="border: 1px solid #555;">
      <img src="defay_1x9/pics_readme/Gitler_Prime.jpg" width="100" height="100" style="border-radius: 50%" alt="avatar"><br />
      <b>Максим Землянский</b><br />
      <sub><i>Backend, Pintest</i></sub>
      <hr style="border: 1px solid #555; margin: 10px 0;">
      <div align="left">
      <b>Вклад в проект:</b><br />
      • Безпосаность<br />
      • Придумывал проблемы<br />
      <hr style="border: 1px solid #555; margin: 10px 0;">
      <b>Контакты:</b><br />
      <a href="https://github.com/kusotsu">GitHub</a> • <a href="https://t.me/kusotsutar">Telegram</a>
      </div>
    </td>
  </tr>
</table>

![alt text](defay_1x9/pics_readme/image.jpg)