"""
Factories for creating test data
"""

import factory
from factory.alchemy import SQLAlchemyModelFactory
from faker import Faker
from datetime import datetime, timedelta
import random

from bookstore.models import User, Author, Genre, Book, Review, ReadingList
from bookstore.auth import get_password_hash

fake = Faker(['ru_RU', 'en_US'])


class UserFactory(SQLAlchemyModelFactory):
    """Factory for creating users"""
    
    class Meta:
        model = User
        sqlalchemy_session_persistence = "commit"
    
    email = factory.LazyAttribute(lambda obj: fake.unique.email())
    username = factory.LazyAttribute(lambda obj: fake.unique.user_name())
    full_name = factory.LazyAttribute(lambda obj: fake.name())
    hashed_password = factory.LazyAttribute(lambda obj: get_password_hash("testpass123"))
    is_active = True
    is_superuser = False


class SuperUserFactory(UserFactory):
    """Factory for creating superusers"""
    is_superuser = True
    username = factory.Sequence(lambda n: f"admin{n}")
    email = factory.Sequence(lambda n: f"admin{n}@example.com")


class AuthorFactory(SQLAlchemyModelFactory):
    """Factory for creating authors"""
    
    class Meta:
        model = Author
        sqlalchemy_session_persistence = "commit"
    
    name = factory.LazyAttribute(lambda obj: fake.name())
    biography = factory.LazyAttribute(lambda obj: fake.text(max_nb_chars=500))
    nationality = factory.LazyAttribute(lambda obj: fake.country())
    birth_date = factory.LazyAttribute(
        lambda obj: fake.date_between(start_date='-100y', end_date='-20y')
    )
    death_date = factory.LazyAttribute(
        lambda obj: fake.date_between(start_date='-20y', end_date='today') 
        if random.choice([True, False]) else None
    )


class GenreFactory(SQLAlchemyModelFactory):
    """Factory for creating genres"""
    
    class Meta:
        model = Genre
        sqlalchemy_session_persistence = "commit"
    
    name = factory.LazyAttribute(lambda obj: fake.unique.word().title())
    description = factory.LazyAttribute(lambda obj: fake.text(max_nb_chars=200))


class BookFactory(SQLAlchemyModelFactory):
    """Factory for creating books"""
    
    class Meta:
        model = Book
        sqlalchemy_session_persistence = "commit"
    
    title = factory.LazyAttribute(lambda obj: fake.sentence(nb_words=4).rstrip('.'))
    description = factory.LazyAttribute(lambda obj: fake.text(max_nb_chars=1000))
    isbn = factory.LazyAttribute(lambda obj: fake.isbn13())
    publication_date = factory.LazyAttribute(
        lambda obj: fake.date_between(start_date='-50y', end_date='today')
    )
    page_count = factory.LazyAttribute(lambda obj: fake.random_int(min=50, max=1500))
    language = factory.LazyAttribute(lambda obj: fake.random_element(['ru', 'en', 'fr', 'de']))
    price = factory.LazyAttribute(lambda obj: round(fake.pyfloat(min_value=9.99, max_value=999.99, right_digits=2), 2))
    cover_image_url = factory.LazyAttribute(lambda obj: fake.image_url())
    is_available = factory.LazyAttribute(lambda obj: fake.boolean(chance_of_getting_true=90))
    
    # Many-to-many relationships
    @factory.post_generation
    def authors(self, create, extracted, **kwargs):
        if not create:
            return
        
        if extracted:
            for author in extracted:
                self.authors.append(author)
        else:
            # Create 1-3 authors by default
            author_count = fake.random_int(min=1, max=3)
            for _ in range(author_count):
                author = AuthorFactory()
                self.authors.append(author)
    
    @factory.post_generation
    def genres(self, create, extracted, **kwargs):
        if not create:
            return
        
        if extracted:
            for genre in extracted:
                self.genres.append(genre)
        else:
            # Create 1-2 genres by default
            genre_count = fake.random_int(min=1, max=2)
            for _ in range(genre_count):
                genre = GenreFactory()
                self.genres.append(genre)


class ReviewFactory(SQLAlchemyModelFactory):
    """Factory for creating reviews"""
    
    class Meta:
        model = Review
        sqlalchemy_session_persistence = "commit"
    
    user = factory.SubFactory(UserFactory)
    book = factory.SubFactory(BookFactory)
    rating = factory.LazyAttribute(lambda obj: fake.random_int(min=1, max=5))
    title = factory.LazyAttribute(lambda obj: fake.sentence(nb_words=6).rstrip('.'))
    content = factory.LazyAttribute(lambda obj: fake.text(max_nb_chars=500))


class ReadingListFactory(SQLAlchemyModelFactory):
    """Factory for creating reading lists"""
    
    class Meta:
        model = ReadingList
        sqlalchemy_session_persistence = "commit"
    
    user = factory.SubFactory(UserFactory)
    name = factory.LazyAttribute(lambda obj: fake.sentence(nb_words=3).rstrip('.'))
    description = factory.LazyAttribute(lambda obj: fake.text(max_nb_chars=300))
    is_public = factory.LazyAttribute(lambda obj: fake.boolean(chance_of_getting_true=30))


# Special factories for test scenarios

class PopularBookFactory(BookFactory):
    """Factory for popular books"""
    price = factory.LazyAttribute(lambda obj: round(fake.pyfloat(min_value=299.99, max_value=799.99, right_digits=2), 2))
    page_count = factory.LazyAttribute(lambda obj: fake.random_int(min=300, max=800))
    is_available = True


class ClassicBookFactory(BookFactory):
    """Factory for classic books"""
    publication_date = factory.LazyAttribute(
        lambda obj: fake.date_between(start_date='-200y', end_date='-50y')
    )
    page_count = factory.LazyAttribute(lambda obj: fake.random_int(min=200, max=1000))
    language = 'ru'


class NewBookFactory(BookFactory):
    """Factory for new books"""
    publication_date = factory.LazyAttribute(
        lambda obj: fake.date_between(start_date='-2y', end_date='today')
    )
    is_available = True


class ExpensiveBookFactory(BookFactory):
    """Factory for expensive books"""
    price = factory.LazyAttribute(lambda obj: round(fake.pyfloat(min_value=500.0, max_value=2000.0, right_digits=2), 2))


class FreeBookFactory(BookFactory):
    """Factory for free books"""
    price = 0.0


# Batch factories for creating multiple objects

def create_test_library(db_session, num_books=50):
    """Create test library"""
    # Configure all factories to work with passed session
    UserFactory._meta.sqlalchemy_session = db_session
    SuperUserFactory._meta.sqlalchemy_session = db_session
    AuthorFactory._meta.sqlalchemy_session = db_session
    GenreFactory._meta.sqlalchemy_session = db_session
    BookFactory._meta.sqlalchemy_session = db_session
    ReviewFactory._meta.sqlalchemy_session = db_session
    ReadingListFactory._meta.sqlalchemy_session = db_session
    
    # Create users
    users = UserFactory.create_batch(10)
    admin = SuperUserFactory()
    
    # Create authors and genres
    authors = AuthorFactory.create_batch(20)
    genres = GenreFactory.create_batch(10)
    
    # Create books
    books = []
    for _ in range(num_books):
        book_authors = fake.random_elements(authors, length=fake.random_int(1, 3), unique=True)
        book_genres = fake.random_elements(genres, length=fake.random_int(1, 2), unique=True)
        
        book = BookFactory(authors=book_authors, genres=book_genres)
        books.append(book)
    
    # Create reviews
    for _ in range(min(num_books * 2, 100)):  # Limit number of reviews
        user = fake.random_element(users)
        book = fake.random_element(books)
        
        # Check that user hasn't already left a review for this book
        existing_review = db_session.query(Review).filter(
            Review.user_id == user.id,
            Review.book_id == book.id
        ).first()
        
        if not existing_review:
            ReviewFactory(user=user, book=book)
    
    # Create reading lists (simplified)
    for user in users[:5]:  # Only for first 5 users
        if fake.boolean(chance_of_getting_true=70):  # 70% of users have lists
            reading_list = ReadingListFactory(user=user)
            
            # Add books to list
            list_books = fake.random_elements(books, length=fake.random_int(3, 10), unique=True)
            for book in list_books:
                from bookstore.models import ReadingListItem
                item = ReadingListItem(
                    reading_list_id=reading_list.id,
                    book_id=book.id,
                    notes=fake.sentence() if fake.boolean() else None
                )
                db_session.add(item)
    
    db_session.commit()
    
    return {
        'users': users,
        'admin': admin,
        'authors': authors,
        'genres': genres,
        'books': books
    }