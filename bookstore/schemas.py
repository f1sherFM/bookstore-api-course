"""
Pydantic schemas for data validation
"""

from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Union
from datetime import datetime
from enum import Enum


# Base schemas
class TimestampMixin(BaseModel):
    """Mixin for timestamps"""
    created_at: datetime
    updated_at: Optional[datetime] = None


# Users
class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: Optional[str] = Field(None, max_length=255)
    is_active: bool = True


class UserCreate(UserBase):
    """Schema for user creation"""
    password: str = Field(..., min_length=8, max_length=100)


class UserUpdate(BaseModel):
    """Schema for user update"""
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    full_name: Optional[str] = Field(None, max_length=255)
    is_active: Optional[bool] = None


class UserInDB(UserBase, TimestampMixin):
    """User schema in DB"""
    class Config:
        from_attributes = True
    
    id: int
    is_superuser: bool = False


class User(UserInDB):
    """Public user schema"""
    pass


# Authors
class AuthorBase(BaseModel):
    """Base author schema"""
    name: str = Field(..., min_length=1, max_length=255)
    biography: Optional[str] = None
    birth_date: Optional[datetime] = None
    death_date: Optional[datetime] = None
    nationality: Optional[str] = Field(None, max_length=100)


class AuthorCreate(AuthorBase):
    """Schema for author creation"""
    pass


class AuthorUpdate(BaseModel):
    """Schema for author update"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    biography: Optional[str] = None
    birth_date: Optional[datetime] = None
    death_date: Optional[datetime] = None
    nationality: Optional[str] = Field(None, max_length=100)


class Author(AuthorBase, TimestampMixin):
    """Author schema"""
    class Config:
        from_attributes = True
    
    id: int


# Genres
class GenreBase(BaseModel):
    """Base genre schema"""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None


class GenreCreate(GenreBase):
    """Schema for genre creation"""
    pass


class GenreUpdate(BaseModel):
    """Schema for genre update"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None


class Genre(GenreBase):
    """Genre schema"""
    class Config:
        from_attributes = True
    
    id: int
    created_at: datetime


# Books
class BookBase(BaseModel):
    """Base book schema"""
    title: str = Field(..., min_length=1, max_length=500)
    isbn: Optional[str] = Field(None, max_length=20)
    description: Optional[str] = None
    publication_date: Optional[datetime] = None
    page_count: Optional[int] = Field(None, gt=0)
    language: str = Field(default="ru", max_length=10)
    price: Optional[float] = Field(None, ge=0)
    cover_image_url: Optional[str] = Field(None, max_length=500)
    is_available: bool = True


class BookCreate(BookBase):
    """Schema for book creation"""
    author_ids: List[int] = Field(..., min_items=1)
    genre_ids: List[int] = Field(..., min_items=1)


class BookUpdate(BaseModel):
    """Schema for book update"""
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    isbn: Optional[str] = Field(None, max_length=20)
    description: Optional[str] = None
    publication_date: Optional[datetime] = None
    page_count: Optional[int] = Field(None, gt=0)
    language: Optional[str] = Field(None, max_length=10)
    price: Optional[float] = Field(None, ge=0)
    cover_image_url: Optional[str] = Field(None, max_length=500)
    is_available: Optional[bool] = None
    author_ids: Optional[List[int]] = None
    genre_ids: Optional[List[int]] = None


class Book(BookBase, TimestampMixin):
    """Book schema"""
    class Config:
        from_attributes = True
    
    id: int
    authors: List[Author] = []
    genres: List[Genre] = []


class BookWithStats(Book):
    """Book with statistics"""
    average_rating: Optional[float] = None
    review_count: int = 0


# Reviews
class ReviewBase(BaseModel):
    """Base review schema"""
    rating: int = Field(..., ge=1, le=5)
    title: Optional[str] = Field(None, max_length=255)
    content: Optional[str] = None


class ReviewCreate(ReviewBase):
    """Schema for review creation"""
    book_id: int


class ReviewUpdate(BaseModel):
    """Schema for review update"""
    rating: Optional[int] = Field(None, ge=1, le=5)
    title: Optional[str] = Field(None, max_length=255)
    content: Optional[str] = None


class Review(ReviewBase, TimestampMixin):
    """Review schema"""
    class Config:
        from_attributes = True
    
    id: int
    user_id: int
    book_id: int
    user: User
    book: Book


# Reading lists
class ReadingListBase(BaseModel):
    """Base reading list schema"""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    is_public: bool = False


class ReadingListCreate(ReadingListBase):
    """Schema for reading list creation"""
    pass


class ReadingListUpdate(BaseModel):
    """Schema for reading list update"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    is_public: Optional[bool] = None


class ReadingListItemBase(BaseModel):
    """Base reading list item schema"""
    book_id: int
    notes: Optional[str] = None


class ReadingListItemCreate(ReadingListItemBase):
    """Schema for adding book to list"""
    pass


class ReadingListItem(ReadingListItemBase):
    """Reading list item schema"""
    class Config:
        from_attributes = True
    
    id: int
    reading_list_id: int
    added_at: datetime
    book: Book


class ReadingList(ReadingListBase, TimestampMixin):
    """Reading list schema"""
    class Config:
        from_attributes = True
    
    id: int
    user_id: int
    user: User
    items: List[ReadingListItem] = []


# Authentication
class Token(BaseModel):
    """Token schema"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token data"""
    username: Optional[str] = None


class LoginRequest(BaseModel):
    """Login request"""
    username: str
    password: str


# Search and filtering
class BookSearchParams(BaseModel):
    """Book search parameters"""
    q: Optional[str] = Field(None, description="Search query")
    author: Optional[str] = Field(None, description="Author name")
    genre: Optional[str] = Field(None, description="Genre")
    min_price: Optional[float] = Field(None, ge=0, description="Minimum price")
    max_price: Optional[float] = Field(None, ge=0, description="Maximum price")
    language: Optional[str] = Field(None, description="Language")
    available_only: bool = Field(True, description="Only available books")


class SortOrder(str, Enum):
    """Sort order"""
    ASC = "asc"
    DESC = "desc"


class BookSortBy(str, Enum):
    """Book sorting fields"""
    TITLE = "title"
    PRICE = "price"
    PUBLICATION_DATE = "publication_date"
    CREATED_AT = "created_at"
    RATING = "rating"


# Pagination
class PaginationParams(BaseModel):
    """Pagination parameters"""
    page: int = Field(1, ge=1, description="Page number")
    size: int = Field(20, ge=1, le=100, description="Page size")


class PaginatedResponse(BaseModel):
    """Paginated response"""
    items: List[Union[Book, Author, Genre, Review, ReadingList]]
    total: int
    page: int
    size: int
    pages: int


# Statistics
class BookStats(BaseModel):
    """Book statistics"""
    total_books: int
    available_books: int
    total_authors: int
    total_genres: int
    average_price: Optional[float]


class UserStats(BaseModel):
    """User statistics"""
    total_users: int
    active_users: int
    total_reviews: int
    total_reading_lists: int