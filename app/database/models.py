"""
SQLAlchemy ORM-модели для проекта Candels (Агневидца).
Построено на основе schema.sql (2025-08-25) и seed_agnevidca.sql.
Используется Declarative Base из session.py.
"""

from sqlalchemy import (
    Column, String, Text, Date, Time, Boolean, Numeric,
    ForeignKey, JSON, TIMESTAMP, Integer
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from .session import Base

# USERS — Telegram-пользователи
class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True)
    telegram_id = Column(String, unique=True, nullable=False)
    telegram_username = Column(String(255))
    ip_address = Column(String(255))
    created_at = Column(TIMESTAMP)

    profiles = relationship("Profile", back_populates="user", cascade="all, delete-orphan")
    subscriptions = relationship("Subscription", back_populates="user", cascade="all, delete-orphan")
    questions = relationship("SupportQuestion", back_populates="user", cascade="all, delete-orphan")
    events = relationship("EventLog", back_populates="user", cascade="all, delete-orphan")
    orders = relationship("CandleOrder", back_populates="user", cascade="all, delete-orphan")
    purchases = relationship("ShopPurchase", back_populates="user", cascade="all, delete-orphan")


# PROFILES — эзотерические профили
class Profile(Base):
    __tablename__ = "profiles"

    id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    name = Column(String(255))
    full_name = Column(String(255))
    whom = Column(String(16))
    birth_date = Column(Date)
    birth_place = Column(String(255))
    birth_time = Column(Time)
    emotion = Column(String(64))
    alignment = Column(String(32))
    zodiac_west = Column(String(32))
    zodiac_east = Column(String(32))
    moon_phase = Column(String(32))
    moon_sign = Column(String(32))
    ascendant = Column(String(32))
    created_at = Column(TIMESTAMP)

    user = relationship("User", back_populates="profiles")
    questions = relationship("SupportQuestion", back_populates="profile")
    orders = relationship("CandleOrder", back_populates="profile")


# SUBSCRIPTIONS — подписки пользователей
class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    type = Column(String(64))
    started_at = Column(TIMESTAMP)
    expires_at = Column(TIMESTAMP)
    daily_limit = Column(Integer, default=10)
    total_queries = Column(Integer, default=0)
    created_at = Column(TIMESTAMP)

    user = relationship("User", back_populates="subscriptions")
    questions = relationship("SupportQuestion", back_populates="subscription")


# SUPPORT QUESTIONS — запросы к Нейромагу
class SupportQuestion(Base):
    __tablename__ = "support_questions"

    id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    profile_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id"))
    subscription_id = Column(UUID(as_uuid=True), ForeignKey("subscriptions.id"))
    message = Column(Text)
    response = Column(Text)
    created_at = Column(TIMESTAMP)

    user = relationship("User", back_populates="questions")
    profile = relationship("Profile", back_populates="questions")
    subscription = relationship("Subscription", back_populates="questions")


# EVENT LOG — аудит действий
class EventLog(Base):
    __tablename__ = "events_log"

    id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    event_type = Column(String(64))
    target_type = Column(String(64))
    target_id = Column(UUID(as_uuid=True))
    metadata = Column(JSONB)
    created_at = Column(TIMESTAMP)

    user = relationship("User", back_populates="events")


# CANDLE ORDERS — заказы свечей
class CandleOrder(Base):
    __tablename__ = "candle_orders"

    id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    profile_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id"))
    type = Column(String(32))
    status = Column(String(32))
    short_result_text = Column(Text)
    full_result_text = Column(Text)
    image_path = Column(String(255))
    pdf_path = Column(String(255))
    delivery_address = Column(Text)
    delivery_service = Column(String(64))
    delivery_tracking = Column(String(64))
    paid = Column(Boolean, default=False)
    price = Column(Numeric(10, 2))
    created_at = Column(TIMESTAMP)

    user = relationship("User", back_populates="orders")
    profile = relationship("Profile", back_populates="orders")
    candle_result = relationship("CandleResult", back_populates="order", uselist=False)


# CANDLE RESULTS — результаты подбора
class CandleResult(Base):
    __tablename__ = "candle_results"

    id = Column(UUID(as_uuid=True), primary_key=True)
    candle_order_id = Column(UUID(as_uuid=True), ForeignKey("candle_orders.id"))
    form = Column(String(64))
    color = Column(String(64))
    aroma = Column(String(64))
    herbs = Column(String(64))
    oils = Column(String(64))
    wax_type = Column(String(64))
    created_at = Column(TIMESTAMP)

    order = relationship("CandleOrder", back_populates="candle_result")


# SHOP PRODUCTS — товары магазина
class ShopProduct(Base):
    __tablename__ = "shop_products"

    id = Column(UUID(as_uuid=True), primary_key=True)
    title = Column(String(255))
    description = Column(Text)
    price = Column(Numeric(10, 2))
    category = Column(String(64))
    active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP)

    purchases = relationship("ShopPurchase", back_populates="product")


# SHOP PURCHASES — покупки пользователей
class ShopPurchase(Base):
    __tablename__ = "shop_purchases"

    id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    product_id = Column(UUID(as_uuid=True), ForeignKey("shop_products.id"))
    quantity = Column(Integer, default=1)
    total_price = Column(Numeric(10, 2))
    paid = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP)

    user = relationship("User", back_populates="purchases")
    product = relationship("ShopProduct", back_populates="purchases")


# Candle Attributes Dictionaries
class CandleShape(Base):
    __tablename__ = "candle_shapes"
    id = Column(String, primary_key=True)
    name = Column(String)
    meaning = Column(Text)
    usage = Column(Text)


class CandleColor(Base):
    __tablename__ = "candle_colors"
    id = Column(String, primary_key=True)
    name = Column(String)
    meaning = Column(Text)
    usage = Column(Text)


class CandleHerb(Base):
    __tablename__ = "candle_herbs"
    id = Column(String, primary_key=True)
    name = Column(String)
    meaning = Column(Text)
    usage = Column(Text)


class CandleOil(Base):
    __tablename__ = "candle_oils"
    id = Column(String, primary_key=True)
    name = Column(String)
    meaning = Column(Text)
    usage = Column(Text)


class Holiday(Base):
    __tablename__ = "holidays"
    id = Column(String, primary_key=True)
    name = Column(String)


class Event(Base):
    __tablename__ = "events"
    id = Column(String, primary_key=True)
    name = Column(String)