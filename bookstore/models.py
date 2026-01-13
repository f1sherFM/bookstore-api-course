"""
Database Models - SQLAlchemy ORM Definitions

This file defines the database structure for our BookStore API using SQLAlchemy ORM.
ORM (Object-Relational Mapping) allows us to work with database tables as Python classes.

Key Concepts for Beginners:
- Each class represents a database table
- Each class attribute represents a table column
- Relationships define how tables are connected
- SQLAlchemy handles the SQL generation automatically

Database Tables in our BookStore:
- users: People who use our bookstore
- authors: Writers of books
- genres: Categories of books (fiction, non-fiction, etc.)
- books: The actual books in our store
- reviews: User reviews and ratings for books
- reading_lists: Personal book collections for users
- reading_list_items: Books within a reading list

Relationships:
- Books can have multiple authors (many-to-many)
- Books can belong to multiple genres (many-to-many)
- Users can write multiple reviews (one-to-many)
- Users can have multiple reading lists (one-to-many)
"""

# Import SQLAlchemy components
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, Boolean, Table
from sqlalchemy.ext.declarative import declarative_base  # Base class for all models
from sqlalchemy.orm import relationship  # Define relationships between tables
from sqlalchemy.sql import func  # SQL functions like NOW(), COUNT(), etc.
from datetime import datetime

# Create the base class that all our models will inherit from
Base = declarative_base()

# Many-to-Many Relationship Tables
# These tables connect two other tables when one record can relate to many records in another table

# Books ↔ Authors relationship (a book can have multiple authors, an author can write multiple books)
book_authors = Table(
    'book_authors',  # Table name in the database
    Base.metadata,   # Metadata from our base class
    Column('book_id', Integer, ForeignKey('books.id'), primary_key=True),    # Reference to books table
    Column('author_id', Integer, ForeignKey('authors.id'), primary_key=True) # Reference to authors table
)

# Books ↔ Genres relationship (a book can belong to multiple genres, a genre can contain multiple books)
book_genres = Table(
    'book_genres',   # Table name in the database
    Base.metadata,   # Metadata from our base class
    Column('book_id', Integer, ForeignKey('books.id'), primary_key=True),   # Reference to books table
    Column('genre_id', Integer, ForeignKey('genres.id'), primary_key=True)  # Reference to genres table
)


class User(Base):
    """
    User Model - Represents people who use our bookstore
    
    This model stores information about users who can:
    - Browse and search books
    - Write reviews
    - Create reading lists
    - Authenticate with the system
    
    Security Features:
    - Passwords are hashed (never stored in plain text)
    - Users can be activated/deactivated
    - Superuser flag for admin privileges
    
    For beginners: Think of this as a "user account" in any app you use.
    It stores your email, username, and other profile information.
    """
    __tablename__ = "users"  # Name of the table in the database
    
    # Primary key - unique identifier for each user
    id = Column(Integer, primary_key=True, index=True)
    
    # User credentials and contact information
    email = Column(String(255), unique=True, index=True, nullable=False)        # Must be unique and not empty
    username = Column(String(100), unique=True, index=True, nullable=False)     # Must be unique and not empty
    full_name = Column(String(255), nullable=True)                              # Optional full name
    hashed_password = Column(String(255), nullable=False)                       # Encrypted password (never plain text!)
    
    # User status and permissions
    is_active = Column(Boolean, default=True)      # Can the user log in?
    is_superuser = Column(Boolean, default=False)  # Does the user have admin privileges?
    
    # Additional user information
    phone_number = Column(String(20), nullable=True)  # Optional phone number (added for Alembic migration example)
    
    # Automatic timestamps
    created_at = Column(DateTime, default=func.now())    # When the user account was created
    updated_at = Column(DateTime, onupdate=func.now())   # When the user account was last modified
    
    # Relationships to other tables
    # These create "virtual" attributes that let us access related data easily
    reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")
    # ↑ user.reviews gives us all reviews written by this user
    # cascade="all, delete-orphan" means if we delete a user, delete their reviews too
    
    reading_lists = relationship("ReadingList", back_populates="user", cascade="all, delete-orphan")
    # ↑ user.reading_lists gives us all reading lists created by this user


class Author(Base):
    """
    Author Model - Represents writers and creators of books
    
    This model stores information about book authors including:
    - Basic biographical information
    - Birth and death dates
    - Nationality
    - Biography text
    
    For beginners: This is like an "author profile" that contains
    information about the people who write the books in our store.
    """
    __tablename__ = "authors"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Author information
    name = Column(String(255), nullable=False, index=True)  # Author's name (required, searchable)
    biography = Column(Text, nullable=True)                 # Long text about the author's life and work
    birth_date = Column(DateTime, nullable=True)            # When the author was born
    death_date = Column(DateTime, nullable=True)            # When the author died (if applicable)
    nationality = Column(String(100), nullable=True)       # Author's country/nationality
    
    # Automatic timestamps
    created_at = Column(DateTime, default=func.now())      # When this author record was created
    updated_at = Column(DateTime, onupdate=func.now())     # When this author record was last updated
    
    # Relationships
    books = relationship("Book", secondary=book_authors, back_populates="authors")
    # ↑ author.books gives us all books written by this author
    # secondary=book_authors means this relationship goes through the book_authors junction table


class Genre(Base):
    """
    Genre Model - Represents categories or types of books
    
    Genres help organize books into categories like:
    - Fiction, Non-fiction
    - Mystery, Romance, Science Fiction
    - Biography, History, etc.
    
    For beginners: Think of genres like "sections" in a bookstore
    or library - they help people find the type of books they want.
    """
    __tablename__ = "genres"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Genre information
    name = Column(String(100), unique=True, nullable=False, index=True)  # Genre name (must be unique)
    description = Column(Text, nullable=True)                            # Description of what this genre includes
    
    # Timestamp
    created_at = Column(DateTime, default=func.now())  # When this genre was created
    
    # Relationships
    books = relationship("Book", secondary=book_genres, back_populates="genres")
    # ↑ genre.books gives us all books in this genre
    # secondary=book_genres means this relationship goes through the book_genres junction table


class Book(Base):
    """
    Book Model - Represents books in our bookstore
    
    This is the central model of our bookstore system. It contains:
    - Basic book information (title, description, etc.)
    - Publication details (date, page count, language)
    - Commercial information (price, availability)
    - Metadata (ISBN, cover image)
    
    Relationships:
    - Connected to authors (who wrote it)
    - Connected to genres (what category it belongs to)
    - Connected to reviews (what users think about it)
    - Connected to reading lists (users' personal collections)
    
    For beginners: This represents an actual book you might buy in a bookstore.
    It has all the information you'd see on a book's back cover or product page.
    """
    __tablename__ = "books"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Basic book information
    title = Column(String(500), nullable=False, index=True)  # Book title (required, searchable)
    isbn = Column(String(20), unique=True, nullable=True, index=True)  # International Standard Book Number (unique identifier)
    description = Column(Text, nullable=True)                # Book summary/description
    
    # Publication information
    publication_date = Column(DateTime, nullable=True)       # When the book was published
    page_count = Column(Integer, nullable=True)              # Number of pages
    language = Column(String(10), default="ru")              # Language code (defaults to Russian)
    
    # Commercial information
    price = Column(Float, nullable=True)                     # Book price
    is_available = Column(Boolean, default=True)             # Is the book currently available for purchase?
    
    # Media and presentation
    cover_image_url = Column(String(500), nullable=True)     # URL to book cover image
    
    # Automatic timestamps
    created_at = Column(DateTime, default=func.now())        # When this book record was created
    updated_at = Column(DateTime, onupdate=func.now())       # When this book record was last updated
    
    # Relationships to other tables
    authors = relationship("Author", secondary=book_authors, back_populates="books")
    # ↑ book.authors gives us all authors who wrote this book
    
    genres = relationship("Genre", secondary=book_genres, back_populates="books")
    # ↑ book.genres gives us all genres this book belongs to
    
    reviews = relationship("Review", back_populates="book", cascade="all, delete-orphan")
    # ↑ book.reviews gives us all reviews written for this book
    # If we delete a book, delete all its reviews too
    
    reading_list_items = relationship("ReadingListItem", back_populates="book", cascade="all, delete-orphan")
    # ↑ book.reading_list_items shows which reading lists contain this book
    # If we delete a book, remove it from all reading lists


class Review(Base):
    """
    Review Model - Represents user reviews and ratings for books
    
    This model allows users to:
    - Rate books on a 1-5 star scale
    - Write detailed reviews
    - Share their opinions about books
    
    Business Rules:
    - Each user can only review a book once
    - Ratings must be between 1 and 5 stars
    - Reviews can have both a title and detailed content
    
    For beginners: This is like a "customer review" on Amazon or other
    e-commerce sites where people share their opinions about products.
    """
    __tablename__ = "reviews"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys - connect this review to a user and a book
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Who wrote this review
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)  # Which book is being reviewed
    
    # Review content
    rating = Column(Integer, nullable=False)        # Star rating (1-5, validated in schemas)
    title = Column(String(255), nullable=True)     # Optional review title
    content = Column(Text, nullable=True)          # Optional detailed review text
    
    # Automatic timestamps
    created_at = Column(DateTime, default=func.now())  # When the review was written
    updated_at = Column(DateTime, onupdate=func.now()) # When the review was last edited
    
    # Relationships - connect back to the user and book
    user = relationship("User", back_populates="reviews")
    # ↑ review.user gives us the user who wrote this review
    
    book = relationship("Book", back_populates="reviews")
    # ↑ review.book gives us the book being reviewed


class ReadingList(Base):
    """
    Reading List Model - Represents user-created collections of books
    
    This model allows users to:
    - Create personal book collections (like "Want to Read", "Favorites")
    - Organize books by themes or purposes
    - Share lists publicly or keep them private
    - Add notes and descriptions to their lists
    
    For beginners: This is like creating a "playlist" but for books.
    Users can group books together for any reason - books they want to read,
    books they've finished, books for a specific topic, etc.
    """
    __tablename__ = "reading_lists"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign key - which user owns this list
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # List information
    name = Column(String(255), nullable=False)      # Name of the reading list (e.g., "Summer Reading")
    description = Column(Text, nullable=True)       # Optional description of the list's purpose
    is_public = Column(Boolean, default=False)      # Can other users see this list?
    
    # Automatic timestamps
    created_at = Column(DateTime, default=func.now())  # When the list was created
    updated_at = Column(DateTime, onupdate=func.now()) # When the list was last modified
    
    # Relationships
    user = relationship("User", back_populates="reading_lists")
    # ↑ reading_list.user gives us the user who owns this list
    
    items = relationship("ReadingListItem", back_populates="reading_list", cascade="all, delete-orphan")
    # ↑ reading_list.items gives us all books in this list
    # If we delete a reading list, delete all its items too


class ReadingListItem(Base):
    """
    Reading List Item Model - Represents a book within a reading list
    
    This is a "junction" model that connects books to reading lists.
    It allows us to:
    - Track which books are in which lists
    - Record when a book was added to a list
    - Add personal notes about why the book is in the list
    
    For beginners: If ReadingList is like a "playlist", then ReadingListItem
    is like an individual "song" in that playlist. It connects a specific book
    to a specific reading list and can store additional information about
    why it's there.
    """
    __tablename__ = "reading_list_items"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys - connect to the reading list and the book
    reading_list_id = Column(Integer, ForeignKey("reading_lists.id"), nullable=False)  # Which list
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)                  # Which book
    
    # Item-specific information
    added_at = Column(DateTime, default=func.now())  # When this book was added to the list
    notes = Column(Text, nullable=True)              # Optional personal notes about this book
    
    # Relationships
    reading_list = relationship("ReadingList", back_populates="items")
    # ↑ item.reading_list gives us the reading list this item belongs to
    
    book = relationship("Book", back_populates="reading_list_items")
    # ↑ item.book gives us the actual book object