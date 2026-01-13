"""Flask Roadmap API Application."""

from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

# Initialize extensions
db = SQLAlchemy()


def create_app(config_name='development'):
    """Create and configure Flask application."""
    app = Flask(__name__)
    
    # Load configuration
    if config_name == 'development':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///roadmap.db'
        app.config['DEBUG'] = True
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///roadmap.db'
        app.config['DEBUG'] = False
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
    
    # Initialize extensions with app
    db.init_app(app)
    CORS(app)
    
    # Register blueprints
    from app.routes.api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1')
    
    # Serve static files and demo page
    @app.route('/')
    def index():
        """Serve the demo page."""
        static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'static')
        return send_from_directory(static_dir, 'index.html')
    
    @app.route('/static/<path:filename>')
    def static_files(filename):
        """Serve static files."""
        static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'static')
        return send_from_directory(static_dir, filename)
    
    # Create tables
    with app.app_context():
        db.create_all()
        
        # Seed data if tables are empty
        from app.models.node import Node
        try:
            if Node.query.count() == 0:
                from app.utils.seed_data import create_bookstore_roadmap
                create_bookstore_roadmap()
        except Exception as e:
            # If there's an error (like missing column), recreate everything
            print(f"Database error: {e}")
            print("Recreating database...")
            db.drop_all()
            db.create_all()
            from app.utils.seed_data import create_bookstore_roadmap
            create_bookstore_roadmap()
    
    return app