"""
Basic unit tests
"""

import pytest
from datetime import datetime, timedelta
from bookstore.auth import (
    get_password_hash, verify_password, create_access_token,
    get_user_by_username, authenticate_user
)
from bookstore.models import User, Book, Author, Genre


class TestPasswordHashing:
    """Password hashing tests"""
    
    def test_password_hashing(self):
        """Test password hashing"""
        password = "testpassword123"
        hashed = get_password_hash(password)
        
        assert hashed != password
        assert len(hashed) > 20
        assert verify_password(password, hashed)
    
    def test_wrong_password(self):
        """Test wrong password"""
        password = "testpassword123"
        wrong_password = "wrongpassword"
        hashed = get_password_hash(password)
        
        assert not verify_password(wrong_password, hashed)
    
    def test_empty_password(self):
        """Test empty password"""
        with pytest.raises(Exception):
            get_password_hash("")


class TestJWTTokens:
    """JWT token tests"""
    
    def test_create_access_token(self):
        """Test token creation"""
        data = {"sub": "testuser"}
        token = create_access_token(data)
        
        assert isinstance(token, str)
        assert len(token) > 50
        assert "." in token  # JWT contains dots
    
    def test_create_token_with_expiration(self):
        """Test creating token with expiration"""
        data = {"sub": "testuser"}
        expires_delta = timedelta(minutes=15)
        token = create_access_token(data, expires_delta)
        
        assert isinstance(token, str)
        assert len(token) > 50


class TestUserOperations:
    """User operations tests"""
    
    def test_get_user_by_username(self, db_session, test_user):
        """Test getting user by username"""
        user = get_user_by_username(db_session, test_user.username)
        
        assert user is not None
        assert user.username == test_user.username
        assert user.email == test_user.email
    
    def test_get_nonexistent_user(self, db_session):
        """Test getting non-existent user"""
        user = get_user_by_username(db_session, "nonexistent")
        assert user is None
    
    def test_authenticate_user_success(self, db_session, test_user):
        """Test successful authentication"""
        user = authenticate_user(db_session, test_user.username, "testpass123")
        
        assert user is not False
        assert user.username == test_user.username
    
    def test_authenticate_user_wrong_password(self, db_session, test_user):
        """Test authentication with wrong password"""
        user = authenticate_user(db_session, test_user.username, "wrongpassword")
        assert user is False
    
    def test_authenticate_nonexistent_user(self, db_session):
        """Test authentication of non-existent user"""
        user = authenticate_user(db_session, "nonexistent", "password")
        assert user is False


class TestModels:
    """Data model tests"""
    
    def test_user_creation(self, db_session):
        """Test user creation"""
        user = User(
            email="new@example.com",
            username="newuser",
            full_name="New User",
            hashed_password="hashed_password",
            is_active=True
        )
        db_session.add(user)
        db_session.commit()
        
        assert user.id is not None
        assert user.created_at is not None
        assert user.is_superuser is False  # Default value
    
    def test_book_creation(self, db_session, test_author, test_genre):
        """Test book creation"""
        book = Book(
            title="New Book",
            description="New book description",
            price=29.99,
            is_available=True
        )
        book.authors = [test_author]
        book.genres = [test_genre]
        
        db_session.add(book)
        db_session.commit()
        
        assert book.id is not None
        assert book.created_at is not None
        assert len(book.authors) == 1
        assert len(book.genres) == 1
        assert book.authors[0].name == test_author.name
    
    def test_author_book_relationship(self, db_session, test_book, test_author):
        """Test author-book relationship"""
        # Check relationship in both directions
        assert test_author in test_book.authors
        assert test_book in test_author.books
    
    def test_genre_book_relationship(self, db_session, test_book, test_genre):
        """Test genre-book relationship"""
        # Check relationship in both directions
        assert test_genre in test_book.genres
        assert test_book in test_genre.books


class TestValidation:
    """Data validation tests"""
    
    def test_book_price_validation(self):
        """Test book price validation"""
        # Positive price
        book = Book(title="Test", price=10.99)
        assert book.price == 10.99
        
        # Zero price
        book = Book(title="Test", price=0.0)
        assert book.price == 0.0
        
        # Negative price (should be allowed at model level)
        book = Book(title="Test", price=-10.0)
        assert book.price == -10.0
    
    def test_user_email_uniqueness(self, db_session, test_user):
        """Test user email uniqueness"""
        # Try to create user with same email
        duplicate_user = User(
            email=test_user.email,  # Same email
            username="different_username",
            hashed_password="password"
        )
        db_session.add(duplicate_user)
        
        with pytest.raises(Exception):  # Should be uniqueness error
            db_session.commit()
    
    def test_genre_name_uniqueness(self, db_session, test_genre):
        """Test genre name uniqueness"""
        duplicate_genre = Genre(
            name=test_genre.name,  # Same name
            description="Different description"
        )
        db_session.add(duplicate_genre)
        
        with pytest.raises(Exception):  # Should be uniqueness error
            db_session.commit()