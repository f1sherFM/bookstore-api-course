#!/usr/bin/env python3
"""
Create test data for BookStore API
"""

from bookstore.database import SessionLocal
from bookstore.models import User, Author, Genre, Book
from bookstore.auth import get_password_hash

def create_test_data():
    """Create test data"""
    db = SessionLocal()
    try:
        # Check if data already exists
        if db.query(User).first():
            print("Data already exists")
            return
        
        print("Creating test data...")
        
        # Create users
        admin_user = User(
            email="admin@bookstore.com",
            username="admin",
            full_name="Administrator",
            hashed_password=get_password_hash("admin123"),
            is_active=True,
            is_superuser=True
        )
        db.add(admin_user)
        
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
            Author(name="Leo Tolstoy", biography="Russian writer", nationality="Russia"),
            Author(name="Fyodor Dostoevsky", biography="Russian writer", nationality="Russia"),
            Author(name="Alexander Pushkin", biography="Russian poet", nationality="Russia")
        ]
        
        for author in authors:
            db.add(author)
        
        # Create genres
        genres = [
            Genre(name="Classic Literature", description="Works by classic authors"),
            Genre(name="Novel", description="Epic genre"),
            Genre(name="Poetry", description="Poetic works")
        ]
        
        for genre in genres:
            db.add(genre)
        
        # Save to get IDs
        db.commit()
        
        # Create books
        book1 = Book(
            title="War and Peace",
            description="Epic novel about Russian society",
            page_count=1300,
            language="en",
            price=599.99,
            is_available=True
        )
        book1.authors = [authors[0]]  # Leo Tolstoy
        book1.genres = [genres[0], genres[1]]  # Classic, Novel
        db.add(book1)
        
        book2 = Book(
            title="Crime and Punishment",
            description="Psychological novel",
            page_count=671,
            language="en",
            price=449.99,
            is_available=True
        )
        book2.authors = [authors[1]]  # Dostoevsky
        book2.genres = [genres[0], genres[1]]  # Classic, Novel
        db.add(book2)
        
        book3 = Book(
            title="Eugene Onegin",
            description="Novel in verse",
            page_count=384,
            language="en",
            price=299.99,
            is_available=True
        )
        book3.authors = [authors[2]]  # Pushkin
        book3.genres = [genres[0], genres[2]]  # Classic, Poetry
        db.add(book3)
        
        db.commit()
        print("✅ Test data created successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_data()