import logging
import os
import time
from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse
import psycopg2
from psycopg2.errors import UniqueViolation

# Настраиваем базовое логирование
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="Secure App")

# Настройки подключения к PostgreSQL из переменных окружения
DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "secure_db")
DB_USER = os.getenv("DB_USER", "db_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "db_password")

def get_db_connection():
    # ДевОпс-предосторожность: ждем, пока БД поднимется при старте
    for i in range(10):
        try:
            conn = psycopg2.connect(
                host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD
            )
            return conn
        except psycopg2.OperationalError as e:
            logger.warning(f"Database not ready yet (attempt {i+1}/10)... Connecting to {DB_HOST}")
            time.sleep(2)
    raise HTTPException(status_code=500, detail="Database connection failed")

# Инициализация таблицы пользователей при старте приложения
@app.on_event("startup")
def setup_database():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(50) NOT NULL
            );
        """)
        conn.commit()
        cur.close()
        conn.close()
        logger.info("Database table 'users' initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")

# Главная страница с интерфейсом формы
@app.get("/", response_class=HTMLResponse)
def read_root():
    logger.info("Root page accessed")
    return """
    <html>
        <head>
            <title>Secure App UI</title>
            <style>
                body { font-family: 'Segoe UI', Arial, sans-serif; margin: 50px; background: #f0f2f5; color: #333; }
                .card { background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); max-width: 400px; }
                input { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
                button { width: 100%; background: #007bff; color: white; border: none; padding: 12px; border-radius: 4px; cursor: pointer; font-size: 16px; }
                button:hover { background: #0056b3; }
                .danger-link { display: inline-block; margin-top: 20px; color: #dc3545; font-weight: bold; text-decoration: none; }
                .danger-link:hover { text-decoration: underline; }
            </style>
        </head>
        <body>
            <div class="card">
                <h2>🛡️ Secure Application</h2>
                <p>Регистрация нового аккаунта в PostgreSQL:</p>
                <form action="/register" method="post">
                    <input type="text" name="username" placeholder="Придумайте логин" required>
                    <input type="password" name="password" placeholder="Придумайте пароль" required>
                    <button type="submit">Зарегистрироваться</button>
                </form>
                <a href="/admin-panel" class="danger-link">⚠️ Панель администратора (Вход ограничен)</a>
            </div>
        </body>
    </html>
    """

@app.get("/health")
def health_check():
    return {"status": "healthy, testing"}

# Эндпоинт регистрации (Запись в бд)
@app.post("/register")
def register_user(username: str = Form(...), password: str = Form(...)):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        cur.close()
        conn.close()
        logger.info(f"SECURITY EVENT: User '{username}' successfully registered.")
        return HTMLResponse(content=f"<h3>Успех! Пользователь {username} сохранен в БД.</h3><a href='/'>Назад</a>")
    except UniqueViolation:
        logger.warning(f"SECURITY WARNING: Registration failed. Username '{username}' already exists.")
        return HTMLResponse(content="<h3>Ошибка: Логин уже занят!</h3><a href='/'>Назад</a>")

# Наша ИБ-приманка (Генерация 403 ошибки для корреляции в Wazuh)
@app.get("/admin-panel")
def admin_panel():
    logger.error("SECURITY ALERT: Unauthorized access attempt to /admin-panel!")
    raise HTTPException(status_code=403, detail="Access denied. Incident logged.")