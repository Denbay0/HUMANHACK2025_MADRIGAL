from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.database import models, session
from backend.api import auth

app = FastAPI(title="MyApp Backend", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # В продакшене укажите разрешенные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Создаем таблицы в базе данных (если их ещё нет)
models.Base.metadata.create_all(bind=session.engine)

# Подключаем маршруты (роутер аутентификации)
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to MyApp API"}
