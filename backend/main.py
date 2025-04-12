from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.database import models, session
from backend.api import auth, user  # Импортируем оба роутера

app = FastAPI(title="MyApp Backend", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # Для разработки, в продакшене указывайте нужные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Создаем таблицы в базе данных, если их еще нет
models.Base.metadata.create_all(bind=session.engine)

# Регистрируем роутеры
app.include_router(auth.router)
app.include_router(user.router)  # Добавьте регистрацию роутера для user.py

@app.get("/")
def read_root():
    return {"message": "Welcome to MyApp API"}
