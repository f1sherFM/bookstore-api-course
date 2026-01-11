"""
Database configuration using new settings system
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from .models import Base
from .config import settings


def create_database_engine():
    """Create database engine with configuration"""
    db_config = settings.get_database_config()
    
    # SQLite settings
    if db_config["url"].startswith("sqlite"):
        engine = create_engine(
            db_config["url"],
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
            echo=db_config["echo"]
        )
    else:
        # PostgreSQL and other DB settings
        engine = create_engine(
            db_config["url"],
            echo=db_config["echo"],
            pool_size=db_config["pool_size"],
            max_overflow=db_config["max_overflow"],
            pool_timeout=db_config["pool_timeout"],
            pool_recycle=db_config["pool_recycle"]
        )
    
    return engine


# Create engine and session
engine = create_database_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables():
    """Create all tables"""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Dependency for getting DB session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize DB with test data"""
    from .models import User, Author, Genre, Book
    from .auth import get_password_hash
    
    create_tables()
    
    # Skip test data creation in production
    if settings.is_production:
        print("Production environment - skipping test data creation")
        return
    
    db = SessionLocal()
    try:
        # Check if data already exists
        if db.query(User).first():
            print("Database already initialized")
            return
        
        print("Creating test data...")
        
        # Create superuser
        admin_user = User(
            email="admin@bookstore.com",
            username="admin",
            full_name="Administrator",
            hashed_password=get_password_hash("admin123"),
            is_active=True,
            is_superuser=True
        )
        db.add(admin_user)
        
        # Create regular user only in development
        if settings.is_development:
            regular_user = User(
                email="user@example.com",
                username="testuser",
                full_name="Test User",
                hashed_password=get_password_hash("password123"),
                is_active=True,
                is_superuser=False
            )
            db.add(regular_user)
        
        # Create authors
        authors = [
            Author(
                name="Leo Tolstoy",
                biography="Russian writer, philosopher",
                nationality="Russia"
            ),
            Author(
                name="Fyodor Dostoevsky", 
                biography="Russian writer, thinker",
                nationality="Russia"
            ),
            Author(
                name="Alexander Pushkin",
                biography="Russian poet, playwright and prose writer",
                nationality="Russia"
            )
        ]
        
        for author in authors:
            db.add(author)
        
        # Create genres
        genres = [
            Genre(name="Classical Literature", description="Works by classical authors"),
            Genre(name="Novel", description="Epic genre"),
            Genre(name="Poetry", description="Poetic works"),
            Genre(name="Drama", description="Dramatic works"),
            Genre(name="Philosophy", description="Philosophical works")
        ]
        
        for genre in genres:
            db.add(genre)
        
        # Save changes to get IDs
        db.commit()
        
        # Create books only in development
        if settings.is_development:
            books_data = [
                {
                    "title": "War and Peace",
                    "description": "Epic novel about Russian society during the Napoleonic Wars",
                    "page_count": 1300,
                    "language": "ru",
                    "price": 599.99,
                    "author_names": ["Leo Tolstoy"],
                    "genre_names": ["Classical Literature", "Novel"]
                },
                {
                    "title": "Crime and Punishment",
                    "description": "Psychological novel about student Raskolnikov",
                    "page_count": 671,
                    "language": "ru", 
                    "price": 449.99,
                    "author_names": ["Fyodor Dostoevsky"],
                    "genre_names": ["Classical Literature", "Novel"]
                },
                {
                    "title": "Eugene Onegin",
                    "description": "Novel in verse about noble society",
                    "page_count": 384,
                    "language": "ru",
                    "price": 299.99,
                    "author_names": ["Alexander Pushkin"],
                    "genre_names": ["Classical Literature", "Poetry"]
                }
            ]
            
            for book_data in books_data:
                book = Book(
                    title=book_data["title"],
                    description=book_data["description"],
                    page_count=book_data["page_count"],
                    language=book_data["language"],
                    price=book_data["price"],
                    is_available=True
                )
                
                # Add authors
                for author_name in book_data["author_names"]:
                    author = db.query(Author).filter(Author.name == author_name).first()
                    if author:
                        book.authors.append(author)
                
                # Add genres
                for genre_name in book_data["genre_names"]:
                    genre = db.query(Genre).filter(Genre.name == genre_name).first()
                    if genre:
                        book.genres.append(genre)
                
                db.add(book)
        
        db.commit()
        print("Test data created successfully!")
        
    except Exception as e:
        print(f"Error creating test data: {e}")
        db.rollback()
    finally:
        db.close()


def get_database_info():
    """Get database information for health check"""
    try:
        db = SessionLocal()
        result = db.execute("SELECT 1").scalar()
        db.close()
        return {"status": "healthy", "connection": "ok"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}