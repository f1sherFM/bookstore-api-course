-- Инициализация базы данных BookStore
-- Этот файл выполняется при первом запуске PostgreSQL контейнера

-- Создание расширений
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Создание индексов для оптимизации производительности
-- (Таблицы будут созданы SQLAlchemy, здесь только дополнительные индексы)

-- Функция для обновления updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Комментарий о готовности базы данных
SELECT 'BookStore database initialized successfully' as status;