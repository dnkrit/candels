"""
CRUD-модуль для проекта Candels.
Описывает операции создания, чтения, обновления и удаления
для таблиц user_profiles, runes, purposes, emotions и других справочников.
"""

from sqlalchemy.orm import Session
from . import models

# ---------- USER PROFILES ----------

def create_user_profile(db: Session, data: dict):
    user = models.Profile(**data)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_profile(db: Session, user_id: str):
    return db.query(models.Profile).filter(models.Profile.id == user_id).first()


def get_all_users(db: Session):
    return db.query(models.Profile).all()


def update_user_profile(db: Session, user_id: str, data: dict):
    user = db.query(models.Profile).filter(models.Profile.id == user_id).first()
    if not user:
        return None
    for key, value in data.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user


def delete_user_profile(db: Session, user_id: str):
    user = db.query(models.Profile).filter(models.Profile.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user

# ---------- PURPOSES ----------

def create_purpose(db: Session, name: str, description: str = None):
    purpose = models.CandleShape(name=name, meaning=description)
    db.add(purpose)
    db.commit()
    db.refresh(purpose)
    return purpose


def get_purpose(db: Session, name: str):
    return db.query(models.CandleShape).filter(models.CandleShape.name == name).first()

# ---------- EMOTIONS ----------

def get_emotion_by_name(db: Session, name: str):
    return db.query(models.CandleColor).filter(models.CandleColor.name == name).first()


def create_emotion(db: Session, name: str, description: str = None):
    emotion = models.CandleColor(name=name, meaning=description)
    db.add(emotion)
    db.commit()
    db.refresh(emotion)
    return emotion

# ---------- RUNES / SYMBOLS ----------

def get_rune(db: Session, name: str):
    return db.query(models.CandleHerb).filter(models.CandleHerb.name == name).first()


def create_rune(db: Session, name: str, meaning: str):
    rune = models.CandleHerb(name=name, meaning=meaning)
    db.add(rune)
    db.commit()
    db.refresh(rune)
    return rune