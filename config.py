"""
Configuration settings for Flask application.

This file contains all the configuration classes for different environments.
Configuration management is crucial for deploying applications across different environments
(development, testing, production) with different settings.

Key Concepts for Beginners:
- Environment Variables: Settings that can be changed without modifying code
- Configuration Classes: Different settings for different deployment environments
- Security: Secret keys and database URLs should never be hardcoded in production
- Inheritance: Child classes inherit settings from parent Config class
"""

import os


class Config:
    """
    Base configuration class that contains common settings.
    
    This class serves as the parent for all environment-specific configurations.
    It contains settings that are common across all environments.
    
    Key Concepts:
    - Class Variables: These become configuration settings for Flask
    - os.environ.get(): Safely reads environment variables with fallback defaults
    - SECRET_KEY: Used by Flask for session security and CSRF protection
    """
    
    # Secret key for Flask security features (sessions, CSRF protection, etc.)
    # In production, this should ALWAYS come from an environment variable
    # Never hardcode secret keys in production code!
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Disable SQLAlchemy event system to save memory
    # This setting prevents SQLAlchemy from tracking object modifications
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """
    Development configuration for local development.
    
    This configuration is used when developers are working on their local machines.
    It includes settings that make development easier but aren't suitable for production.
    
    Key Features:
    - Debug mode enabled for detailed error messages
    - Local SQLite database for easy setup
    - Relaxed security settings for development convenience
    """
    
    # Enable debug mode for development
    # Debug mode provides detailed error pages and automatic reloading
    # WARNING: Never enable debug mode in production!
    DEBUG = True
    
    # Database URL for development
    # SQLite is used for simplicity - it's a file-based database
    # The database file will be created in the project directory
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///roadmap_dev.db'


class ProductionConfig(Config):
    """
    Production configuration for live deployment.
    
    This configuration is used when the application is deployed to production servers.
    It prioritizes security, performance, and stability over development convenience.
    
    Key Features:
    - Debug mode disabled for security
    - Production database (should be set via environment variable)
    - Enhanced security settings
    """
    
    # Disable debug mode in production for security
    # Debug mode can expose sensitive information to users
    DEBUG = False
    
    # Production database URL
    # In production, this should always come from an environment variable
    # Common production databases: PostgreSQL, MySQL, etc.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///roadmap.db'


class TestingConfig(Config):
    """
    Testing configuration for running automated tests.
    
    This configuration is used when running the test suite.
    It uses settings that make tests run faster and more reliably.
    
    Key Features:
    - Testing mode enabled
    - In-memory database for fast test execution
    - Isolated environment that doesn't affect development data
    """
    
    # Enable testing mode
    # This disables error catching during request handling for better test debugging
    TESTING = True
    
    # Use in-memory SQLite database for tests
    # ':memory:' creates a temporary database that exists only in RAM
    # This makes tests run faster and ensures test isolation
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


# Configuration dictionary for easy access
# This allows the application to select the appropriate configuration
# based on the environment name (e.g., 'development', 'production', 'testing')
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig  # Fallback configuration if none specified
}