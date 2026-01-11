"""
Configuration management system for BookStore API
"""

import os
from typing import List, Optional
from pydantic import validator, Field
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Main application settings"""
    
    # Application Info
    app_name: str = "BookStore API"
    app_version: str = "1.0.0"
    description: str = "Modern book management system"
    
    # Environment
    environment: str = Field(default="development", env="ENVIRONMENT")
    debug: bool = Field(default=False, env="DEBUG")
    
    # Database Configuration
    database_url: str = Field(..., env="DATABASE_URL")
    database_echo: bool = Field(default=False, env="DATABASE_ECHO")
    
    # Redis Configuration
    redis_url: str = Field(default="redis://localhost:6379", env="REDIS_URL")
    redis_password: Optional[str] = Field(default=None, env="REDIS_PASSWORD")
    
    # Security Configuration
    secret_key: str = Field(..., env="SECRET_KEY")
    jwt_secret_key: str = Field(..., env="JWT_SECRET_KEY")
    jwt_expire_minutes: int = Field(default=30, env="JWT_EXPIRE_MINUTES")
    jwt_algorithm: str = Field(default="HS256", env="JWT_ALGORITHM")
    
    # CORS Configuration
    allowed_origins: str = Field(
        default="http://localhost:3000,http://localhost:8080",
        env="ALLOWED_ORIGINS"
    )
    allowed_methods: str = Field(
        default="GET,POST,PUT,DELETE,OPTIONS",
        env="ALLOWED_METHODS"
    )
    allowed_headers: str = Field(
        default="*",
        env="ALLOWED_HEADERS"
    )
    
    # Logging Configuration
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_format: str = Field(default="json", env="LOG_FORMAT")  # json or text
    log_file: Optional[str] = Field(default=None, env="LOG_FILE")
    
    # Performance Configuration
    workers: int = Field(default=4, env="WORKERS")
    max_connections: int = Field(default=100, env="MAX_CONNECTIONS")
    connection_timeout: int = Field(default=30, env="CONNECTION_TIMEOUT")
    
    # Rate Limiting
    rate_limit_per_minute: int = Field(default=60, env="RATE_LIMIT_PER_MINUTE")
    auth_rate_limit_per_minute: int = Field(default=10, env="AUTH_RATE_LIMIT_PER_MINUTE")
    
    # Pagination
    default_page_size: int = Field(default=20, env="DEFAULT_PAGE_SIZE")
    max_page_size: int = Field(default=100, env="MAX_PAGE_SIZE")
    
    # File Upload
    max_file_size: int = Field(default=10 * 1024 * 1024, env="MAX_FILE_SIZE")  # 10MB
    allowed_file_types: str = Field(
        default="image/jpeg,image/png,image/webp",
        env="ALLOWED_FILE_TYPES"
    )
    
    # Cache Configuration
    cache_ttl: int = Field(default=300, env="CACHE_TTL")  # 5 minutes
    cache_enabled: bool = Field(default=True, env="CACHE_ENABLED")
    
    # Monitoring
    metrics_enabled: bool = Field(default=True, env="METRICS_ENABLED")
    health_check_interval: int = Field(default=30, env="HEALTH_CHECK_INTERVAL")
    
    @property
    def allowed_origins_list(self) -> List[str]:
        """Get list of allowed origins"""
        return [origin.strip() for origin in self.allowed_origins.split(",") if origin.strip()]
    
    @property
    def allowed_methods_list(self) -> List[str]:
        """Get list of allowed methods"""
        return [method.strip() for method in self.allowed_methods.split(",") if method.strip()]
    
    @property
    def allowed_headers_list(self) -> List[str]:
        """Get list of allowed headers"""
        if self.allowed_headers == "*":
            return ["*"]
        return [header.strip() for header in self.allowed_headers.split(",") if header.strip()]
    
    @property
    def allowed_file_types_list(self) -> List[str]:
        """Get list of allowed file types"""
        return [file_type.strip() for file_type in self.allowed_file_types.split(",") if file_type.strip()]
    
    @validator("log_level")
    def validate_log_level(cls, v):
        """Log level validation"""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"Log level must be one of: {valid_levels}")
        return v.upper()
    
    @validator("log_format")
    def validate_log_format(cls, v):
        """Log format validation"""
        valid_formats = ["json", "text"]
        if v.lower() not in valid_formats:
            raise ValueError(f"Log format must be one of: {valid_formats}")
        return v.lower()
    
    @validator("environment")
    def validate_environment(cls, v):
        """Environment validation"""
        valid_environments = ["development", "staging", "production", "testing"]
        if v.lower() not in valid_environments:
            raise ValueError(f"Environment must be one of: {valid_environments}")
        return v.lower()
    
    @property
    def is_development(self) -> bool:
        """Check development environment"""
        return self.environment == "development"
    
    @property
    def is_production(self) -> bool:
        """Check production environment"""
        return self.environment == "production"
    
    @property
    def is_testing(self) -> bool:
        """Check testing environment"""
        return self.environment == "testing"
    
    def get_database_config(self) -> dict:
        """Get database configuration"""
        return {
            "url": self.database_url,
            "echo": self.database_echo and self.is_development,
            "pool_size": 5 if self.is_development else 20,
            "max_overflow": 10 if self.is_development else 30,
            "pool_timeout": 30,
            "pool_recycle": 3600,
        }
    
    def get_redis_config(self) -> dict:
        """Get Redis configuration"""
        return {
            "url": self.redis_url,
            "password": self.redis_password,
            "decode_responses": True,
            "socket_timeout": 5,
            "socket_connect_timeout": 5,
            "retry_on_timeout": True,
        }
    
    def get_cors_config(self) -> dict:
        """Get CORS configuration"""
        return {
            "allow_origins": self.allowed_origins_list,
            "allow_credentials": True,
            "allow_methods": self.allowed_methods_list,
            "allow_headers": self.allowed_headers_list,
        }
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


class DevelopmentSettings(Settings):
    """Development settings"""
    environment: str = "development"
    debug: bool = True
    log_level: str = "DEBUG"
    database_echo: bool = True
    
    # More lenient limits for development
    rate_limit_per_minute: int = 1000
    auth_rate_limit_per_minute: int = 100


class StagingSettings(Settings):
    """Staging environment settings"""
    environment: str = "staging"
    debug: bool = False
    log_level: str = "INFO"
    
    # Moderate limits for staging
    rate_limit_per_minute: int = 200
    auth_rate_limit_per_minute: int = 30


class ProductionSettings(Settings):
    """Production environment settings"""
    environment: str = "production"
    debug: bool = False
    log_level: str = "WARNING"
    
    # Strict limits for production
    rate_limit_per_minute: int = 60
    auth_rate_limit_per_minute: int = 10
    
    # Additional validation for production
    @validator("secret_key")
    def validate_production_secret_key(cls, v):
        """Production secret key validation"""
        if len(v) < 32:
            raise ValueError("Secret key must be at least 32 characters in production")
        if v in ["dev-secret-key", "change-me", "your-secret-key-here"]:
            raise ValueError("Must use secure secret key in production")
        return v
    
    @validator("jwt_secret_key")
    def validate_production_jwt_key(cls, v):
        """Production JWT key validation"""
        if len(v) < 32:
            raise ValueError("JWT secret key must be at least 32 characters in production")
        if v in ["dev-jwt-secret", "change-me", "your-jwt-secret-here"]:
            raise ValueError("Must use secure JWT secret key in production")
        return v


class TestingSettings(Settings):
    """Testing settings"""
    environment: str = "testing"
    debug: bool = True
    log_level: str = "DEBUG"
    
    # Test database
    database_url: str = "sqlite:///./test.db"
    
    # Disable external services for tests
    redis_url: str = "redis://localhost:6379/1"  # Separate DB for tests
    cache_enabled: bool = False
    metrics_enabled: bool = False
    
    # Fast JWT tokens for tests
    jwt_expire_minutes: int = 5


@lru_cache()
def get_settings() -> Settings:
    """
    Get application settings with caching
    Automatically selects settings class based on ENVIRONMENT variable
    """
    environment = os.getenv("ENVIRONMENT", "development").lower()
    
    settings_map = {
        "development": DevelopmentSettings,
        "staging": StagingSettings,
        "production": ProductionSettings,
        "testing": TestingSettings,
    }
    
    settings_class = settings_map.get(environment, DevelopmentSettings)
    return settings_class()


# Global settings instance
settings = get_settings()


def reload_settings():
    """Reload settings (useful for tests)"""
    get_settings.cache_clear()
    global settings
    settings = get_settings()
    return settings