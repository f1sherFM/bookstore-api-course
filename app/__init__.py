"""
Flask Roadmap API Application Factory.

This file contains the Flask application factory function and configuration.
The app factory pattern is a best practice that allows creating multiple app instances
with different configurations, making testing and deployment more flexible.

Key Concepts for Beginners:
- App Factory Pattern: A function that creates and configures Flask app instances
- Extensions: Additional functionality added to Flask (database, CORS, etc.)
- Blueprints: A way to organize routes and views into modules
- Application Context: Flask's way of managing request-specific data
- Database Initialization: Setting up tables and seed data automatically
"""

from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
import tempfile

# Initialize Flask extensions
# Extensions are created here but not bound to an app yet (app factory pattern)
# This allows us to create multiple app instances with the same extensions
db = SQLAlchemy()


def create_app(config_name='development'):
    """
    Create and configure Flask application using the app factory pattern.
    
    The app factory pattern is a Flask best practice that allows you to:
    - Create multiple app instances with different configurations
    - Make testing easier by creating isolated app instances
    - Organize configuration and initialization code cleanly
    
    Args:
        config_name (str): The configuration environment to use
                          ('development', 'production', 'testing')
    
    Returns:
        Flask: Configured Flask application instance
    
    Key Concepts:
    - Flask(__name__): Creates a Flask app instance
    - Extensions: Additional functionality (database, CORS) added to Flask
    - Blueprints: Modular way to organize routes and views
    - Application Context: Flask's way to handle request-specific data
    """
    
    # Create Flask application instance
    # __name__ helps Flask locate resources relative to this file
    app = Flask(__name__)
    
    # Load configuration based on environment
    # This is a simplified configuration setup for this project
    # In larger projects, you'd typically use the config.py file more extensively
    if config_name == 'development':
        # Development settings: debug enabled, local SQLite database
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///roadmap.db'
        app.config['DEBUG'] = True
    else:
        # Production settings for Vercel: use in-memory database
        # Vercel serverless functions don't persist files between requests
        # So we use in-memory database and reinitialize data as needed
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['DEBUG'] = False
    
    # Common configuration settings
    # SQLALCHEMY_TRACK_MODIFICATIONS: Disable to save memory (we don't need this feature)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # SECRET_KEY: Used for session security and CSRF protection
    app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
    
    # Initialize extensions with the app instance
    # This binds the extensions to this specific Flask app
    
    # SQLAlchemy: Object-Relational Mapping (ORM) for database operations
    # Allows us to work with database records as Python objects
    db.init_app(app)
    
    # CORS: Cross-Origin Resource Sharing
    # Allows web browsers to make requests to our API from different domains
    # Essential for APIs that will be consumed by web applications
    CORS(app)
    
    # Register blueprints (modular route organization)
    # Blueprints allow us to organize routes into separate modules
    # This keeps the code organized and makes it easier to maintain
    from app.routes.api import api_bp
    # Register the API blueprint with a URL prefix
    # All routes in api_bp will be prefixed with '/api/v1'
    app.register_blueprint(api_bp, url_prefix='/api/v1')
    
    # Static file serving and demo page routes
    # These routes serve the HTML demo interface and static assets
    
    @app.route('/')
    def index():
        """
        Serve the demo page at the root URL.
        
        This route serves the interactive HTML interface that allows users
        to test the API endpoints and visualize the roadmap data.
        
        Returns:
            HTML file: The demo interface (index.html)
        """
        # Get the absolute path to the static directory
        # This ensures the file path works regardless of where the app is run from
        static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'static')
        return send_from_directory(static_dir, 'index.html')
    
    @app.route('/static/<path:filename>')
    def static_files(filename):
        """
        Serve static files (CSS, JS, images, etc.).
        
        This route handles requests for static assets like stylesheets,
        JavaScript files, images, and other resources needed by the demo page.
        
        Args:
            filename (str): The name of the static file to serve
            
        Returns:
            File: The requested static file
        """
        static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'static')
        return send_from_directory(static_dir, filename)
    
    # Database initialization and seeding
    # This section sets up the database tables and populates them with initial data
    with app.app_context():
        """
        Application context is required for database operations.
        
        Flask uses application context to manage request-specific data.
        Database operations need to know which app instance they belong to,
        so we create an application context here.
        """
        
        # Create all database tables based on our models
        # This reads the model definitions and creates the corresponding database tables
        db.create_all()
        
        # Always seed data in production (since we use in-memory database)
        # In development, only seed if empty
        from app.models.node import Node
        should_seed = True
        
        if config_name == 'development':
            try:
                should_seed = Node.query.count() == 0
            except:
                should_seed = True
        
        if should_seed:
            try:
                from app.utils.seed_data import create_bookstore_roadmap
                create_bookstore_roadmap()
                print("Database seeded successfully!")
            except Exception as e:
                print(f"Error seeding database: {e}")
                # Try to recreate tables and seed again
                try:
                    db.drop_all()
                    db.create_all()
                    from app.utils.seed_data import create_bookstore_roadmap
                    create_bookstore_roadmap()
                    print("Database recreated and seeded successfully!")
                except Exception as e2:
                    print(f"Failed to recreate database: {e2}")
    
    # Return the configured Flask application
    return app