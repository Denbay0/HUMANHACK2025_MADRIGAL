# docker/frontend/Dockerfile

# --- ЭТАП 1: Сборка проекта ---
    FROM node:18-alpine AS build

    # Устанавливаем рабочую директорию внутри контейнера
    WORKDIR /app
    
    # Копируем package.json и package-lock.json из проекта
    # (обратите внимание, что путь указывается относительно корня сборочного контекста)
    COPY frontend/my-vite-react-app/package*.json ./
    
    # Устанавливаем зависимости внутри контейнера
    # Вместо npm install можно использовать npm ci, если используется package-lock.json
    RUN npm install
    
    # Копируем весь исходный код фронтенда
    COPY frontend/my-vite-react-app/ .
    
    # Собираем проект в production-режиме
    RUN npm run build
    
    # --- ЭТАП 2: Запуск через Nginx ---
    FROM nginx:1.23-alpine
    
    # Если нужен кастомный конфиг для Nginx (чтобы слушал порт 8000), скопируйте его:
    # Предполагаем, что файл конфигурации находится в docker/frontend/nginx.conf
    COPY docker/frontend/nginx.conf /etc/nginx/nginx.conf
    
    # Копируем скомпилированную сборку из первого этапа
    COPY --from=build /app/dist /usr/share/nginx/html
    
    # Открываем порт 8000
    EXPOSE 8000
    
    # Запускаем Nginx в форграунд-режиме
    CMD ["nginx", "-g", "daemon off;"]
    