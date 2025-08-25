-- SQL Schema for "Агневидца" project
-- Генерация: 2025-08-25 12:56

-- Enable extensions for UUID support
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- USERS: Telegram-пользователи
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    telegram_id BIGINT UNIQUE NOT NULL,
    telegram_username VARCHAR(255),
    ip_address VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- PROFILES: Профили (себя, другого, пары)
CREATE TABLE profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    name VARCHAR(255),
    full_name VARCHAR(255),
    whom VARCHAR(16) CHECK (whom IN ('self', 'him', 'her', 'pair')),
    birth_date DATE,
    birth_place VARCHAR(255),
    birth_time TIME,
    emotion VARCHAR(64),
    alignment VARCHAR(32),
    zodiac_west VARCHAR(32),
    zodiac_east VARCHAR(32),
    moon_phase VARCHAR(32),
    moon_sign VARCHAR(32),
    ascendant VARCHAR(32),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- SUBSCRIPTIONS
CREATE TABLE subscriptions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    type VARCHAR(64), -- e.g., 'Техномагия', 'Pro-гадалка'
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    daily_limit INT DEFAULT 10,
    total_queries INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- SUPPORT QUESTIONS (вопросы к Нейромагу)
CREATE TABLE support_questions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    profile_id UUID REFERENCES profiles(id),
    subscription_id UUID REFERENCES subscriptions(id),
    message TEXT,
    response TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- EVENTS LOG (аудит действий)
CREATE TABLE events_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    event_type VARCHAR(64),
    target_type VARCHAR(64),
    target_id UUID,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- CANDLE ORDERS (заказы свечей)
CREATE TABLE candle_orders (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    profile_id UUID REFERENCES profiles(id),
    type VARCHAR(32), -- individual / gift / pair / custom / shop
    status VARCHAR(32), -- draft / paid / shipped / cancelled
    short_result_text TEXT,
    full_result_text TEXT,
    image_path VARCHAR(255),
    pdf_path VARCHAR(255),
    delivery_address TEXT,
    delivery_service VARCHAR(64),
    delivery_tracking VARCHAR(64),
    paid BOOLEAN DEFAULT FALSE,
    price NUMERIC(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- CANDLE ATTRIBUTES (результаты подбора)
CREATE TABLE candle_results (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    candle_order_id UUID REFERENCES candle_orders(id),
    form VARCHAR(64),
    color VARCHAR(64),
    aroma VARCHAR(64),
    herbs VARCHAR(64),
    oils VARCHAR(64),
    wax_type VARCHAR(64),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- PRODUCTS (магазин, сертификаты, подписки, свечи)
CREATE TABLE shop_products (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(255),
    description TEXT,
    price NUMERIC(10, 2),
    category VARCHAR(64),
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- PURCHASES (покупки в магазине)
CREATE TABLE shop_purchases (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    product_id UUID REFERENCES shop_products(id),
    quantity INT DEFAULT 1,
    total_price NUMERIC(10, 2),
    paid BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);