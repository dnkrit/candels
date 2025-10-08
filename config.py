"""
Конфигурация проекта Candels.
Подключение PostgreSQL через SQLAlchemy и загрузка переменных окружения.
"""

from pydantic import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    BOT_TOKEN: str = os.getenv("BOT_TOKEN")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    class Config:
        env_file = ".env"


settings = Settings()

# SQLAlchemy подключение
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
