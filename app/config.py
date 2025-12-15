import os

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "devboard")
DB_USER = os.getenv("DB_USER", "devboard")
DB_PASSWORD = os.getenv("DB_PASSWORD", "devboard")

DATABASE_URL = os.getenv("DATABASE_URL") or f"sqlite:///./devboard.db"

APP_HOST = os.getenv("APP_HOST", "127.0.0.1")
APP_PORT = int(os.getenv("APP_PORT", 8000))

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
