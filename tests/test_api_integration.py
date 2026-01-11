"""
API integration tests
"""

import pytest
from fastapi import status


class TestAuthenticationAPI:
    """Authentication API tests"""
    
    def test_login_success(self, client, test_user):
        """Test successful login"""
        response = client.post(
            "/auth/login",
            data={"username": test_user.username, "password": "testpass123"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_wrong_password(self, client, test_user):
        """Test login with wrong password"""
        response = client.post(
            "/auth/login",
            data={"username": test_user.username, "password": "wrongpassword"}
        )
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_login_nonexistent_user(self, client):
        """Test login of non-existent user"""
        response = client.post(
            "/auth/login",
            data={"username": "nonexistent", "password": "password"}
        )
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_get_current_user(self, client, auth_headers):
        """Test getting current user"""
        response = client.get("/auth/me", headers=auth_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "username" in data
        assert "email" in data
        assert data["username"] == "testuser"
    
    def test_get_current_user_no_token(self, client):
        """Test getting user without token"""
        response = client.get("/auth/me")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestUsersAPI:
    """Users API tests"""
    
    def test_create_user(self, client):
        """Test user creation"""
        user_data = {
            "email": "newuser@example.com",
            "username": "newuser",
            "full_name": "New User",
            "password": "newpassword123",
            "is_active": True
        }
        
        response = client.post("/api/v1/users/", json=user_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["email"] == user_data["email"]
        assert data["username"] == user_data["username"]
        assert "hashed_password" not in data  # Password should not be returned
    
    def test_create_user_duplicate_email(self, client, test_user):
        """Test creating user with existing email"""
        user_data = {
            "email": test_user.email,  # Existing email
            "username": "differentuser",
            "password": "password123"
        }
        
        response = client.post("/api/v1/users/", json=user_data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Email already registered" in response.json()["detail"]
    
    def test_get_users_as_admin(self, client, admin_headers):
        """Test getting user list as admin"""
        response = client.get("/api/v1/users/", headers=admin_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_users_as_regular_user(self, client, auth_headers):
        """Test getting user list as regular user"""
        response = client.get("/api/v1/users/", headers=auth_headers)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_get_user_profile(self, client, auth_headers):
        """Test getting own profile"""
        response = client.get("/api/v1/users/me", headers=auth_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["username"] == "testuser"


class TestBooksAPI:
    """Books API tests"""
    
    def test_get_books_empty(self, client):
        """Test getting empty book list"""
        response = client.get("/api/v1/books/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0
    
    def test_get_books_with_data(self, client, test_book):
        """Test getting book list with data"""
        response = client.get("/api/v1/books/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == test_book.title
        assert data[0]["price"] == test_book.price
    
    def test_get_book_by_id(self, client, test_book):
        """Test getting book by ID"""
        response = client.get(f"/api/v1/books/{test_book.id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == test_book.id
        assert data["title"] == test_book.title
        assert "authors" in data
        assert "genres" in data
        assert "average_rating" in data
        assert "review_count" in data
    
    def test_get_nonexistent_book(self, client):
        """Test getting non-existent book"""
        response = client.get("/api/v1/books/999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_create_book_as_admin(self, client, admin_headers, test_author, test_genre):
        """Test creating book as admin"""
        book_data = {
            "title": "New Book",
            "description": "New book description",
            "price": 19.99,
            "page_count": 150,
            "language": "en",
            "is_available": True,
            "author_ids": [test_author.id],
            "genre_ids": [test_genre.id]
        }
        
        response = client.post("/api/v1/books/", json=book_data, headers=admin_headers)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["title"] == book_data["title"]
        assert data["price"] == book_data["price"]
    
    def test_create_book_as_regular_user(self, client, auth_headers, test_author, test_genre):
        """Test creating book as regular user"""
        book_data = {
            "title": "New Book",
            "author_ids": [test_author.id],
            "genre_ids": [test_genre.id]
        }
        
        response = client.post("/api/v1/books/", json=book_data, headers=auth_headers)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_search_books(self, client, test_book):
        """Test book search"""
        # Search by title
        response = client.get(f"/api/v1/books/?q={test_book.title}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == test_book.title
    
    def test_filter_books_by_price(self, client, test_book):
        """Test filtering books by price"""
        # Filter by minimum price
        response = client.get(f"/api/v1/books/?min_price={test_book.price - 10}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        
        # Filter by maximum price (excluding)
        response = client.get(f"/api/v1/books/?max_price={test_book.price - 10}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 0


class TestAuthorsAPI:
    """Authors API tests"""
    
    def test_get_authors(self, client, test_author):
        """Test getting author list"""
        response = client.get("/api/v1/authors/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == test_author.name
    
    def test_get_author_by_id(self, client, test_author):
        """Test getting author by ID"""
        response = client.get(f"/api/v1/authors/{test_author.id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == test_author.id
        assert data["name"] == test_author.name
    
    def test_create_author_as_admin(self, client, admin_headers):
        """Test creating author as admin"""
        author_data = {
            "name": "New Author",
            "biography": "New author biography",
            "nationality": "Test Country"
        }
        
        response = client.post("/api/v1/authors/", json=author_data, headers=admin_headers)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["name"] == author_data["name"]
    
    def test_create_author_as_regular_user(self, client, auth_headers):
        """Test creating author as regular user"""
        author_data = {"name": "New Author"}
        
        response = client.post("/api/v1/authors/", json=author_data, headers=auth_headers)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN


class TestGenresAPI:
    """Genres API tests"""
    
    def test_get_genres(self, client, test_genre):
        """Test getting genre list"""
        response = client.get("/api/v1/genres/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == test_genre.name
    
    def test_create_genre_as_admin(self, client, admin_headers):
        """Test creating genre as admin"""
        genre_data = {
            "name": "New Genre",
            "description": "New genre description"
        }
        
        response = client.post("/api/v1/genres/", json=genre_data, headers=admin_headers)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["name"] == genre_data["name"]
    
    def test_create_duplicate_genre(self, client, admin_headers, test_genre):
        """Test creating duplicate genre"""
        genre_data = {
            "name": test_genre.name,  # Existing name
            "description": "Different description"
        }
        
        response = client.post("/api/v1/genres/", json=genre_data, headers=admin_headers)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST