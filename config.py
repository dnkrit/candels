"""
Конфигурация проекта Candels.
Загрузка переменных окружения через Pydantic Settings,
подключение PostgreSQL через SQLAlchemy.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os
import sys

# Загрузка .env файла
load_dotenv()


from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    BOT_TOKEN: str
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    PROJECT_NAME: str = "Candels"

    # 🔽 Дополнительные поля из .env
    ENV: str | None = None
    TIMEZONE: str | None = "Europe/Moscow"
    LOCALE: str | None = "ru_RU"
    DB_HOST: str | None = None
    DB_PORT: str | None = None
    DB_NAME: str | None = None
    DB_USER_BOT: str | None = None
    DB_PASS_BOT: str | None = None
    DB_USER_ANALYTICS: str | None = None
    DB_PASS_ANALYTICS: str | None = None
    ADMINS: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"  # ✅ игнорировать неизвестные поля
    )


    @property
    def sqlalchemy_database_uri(self) -> str:
        """Возвращает нормализованный URI для SQLAlchemy"""
        db_url = self.DATABASE_URL
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql+psycopg2://", 1)
        return db_url


# Инициализация настроек
try:
    settings = Settings()
except Exception as e:
    print("❌ Ошибка загрузки конфигурации:", e)
    sys.exit(1)


# === SQLAlchemy ===
try:
    engine = create_engine(settings.sqlalchemy_database_uri, pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
    print(f"✅ Подключено к БД: {settings.DATABASE_URL.split('@')[-1]}")
except Exception as e:
    print("❌ Ошибка подключения к базе данных:", e)
    sys.exit(1)
