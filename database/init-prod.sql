-- Production database initialization script

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_stat_statements";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create application user (if not exists)
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'bookstore_app') THEN
        CREATE ROLE bookstore_app WITH LOGIN PASSWORD 'secure_app_password';
    END IF;
END
$$;

-- Grant necessary permissions
GRANT CONNECT ON DATABASE bookstore TO bookstore_app;
GRANT USAGE ON SCHEMA public TO bookstore_app;
GRANT CREATE ON SCHEMA public TO bookstore_app;

-- Performance optimizations
ALTER SYSTEM SET shared_preload_libraries = 'pg_stat_statements';
ALTER SYSTEM SET log_statement = 'all';
ALTER SYSTEM SET log_duration = on;
ALTER SYSTEM SET log_min_duration_statement = 1000;

-- Create indexes for common queries (will be created by SQLAlchemy migrations)
-- These are examples of what might be needed

-- Logging table for application logs (optional)
CREATE TABLE IF NOT EXISTS application_logs (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    level VARCHAR(20) NOT NULL,
    service VARCHAR(50) NOT NULL,
    message TEXT NOT NULL,
    request_id UUID,
    user_id INTEGER,
    metadata JSONB
);

-- Index for log queries
CREATE INDEX IF NOT EXISTS idx_application_logs_timestamp ON application_logs(timestamp);
CREATE INDEX IF NOT EXISTS idx_application_logs_level ON application_logs(level);
CREATE INDEX IF NOT EXISTS idx_application_logs_request_id ON application_logs(request_id);

-- Grant permissions on logs table
GRANT SELECT, INSERT ON application_logs TO bookstore_app;
GRANT USAGE ON SEQUENCE application_logs_id_seq TO bookstore_app;