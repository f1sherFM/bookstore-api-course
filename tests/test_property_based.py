"""
Property-based tests with Hypothesis
"""

import pytest
from hypothesis import given, strategies as st, assume, settings, HealthCheck
from hypothesis.strategies import composite
from bookstore.auth import get_password_hash, verify_password
from bookstore.models import User, Book, Author, Genre
from bookstore.schemas import BookCreate, UserCreate


# Strategies for data generation
@composite
def valid_email(draw):
    """Generate valid email addresses"""
    username = draw(st.text(min_size=1, max_size=20, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd'))))
    domain = draw(st.text(min_size=1, max_size=15, alphabet=st.characters(whitelist_categories=('Lu', 'Ll'))))
    tld = draw(st.sampled_from(['com', 'org', 'net', 'edu', 'gov']))
    return f"{username}@{domain}.{tld}"


@composite
def valid_username(draw):
    """Generate valid usernames"""
    return draw(st.text(
        min_size=3, 
        max_size=50, 
        alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd'), whitelist_characters='_-')
    ))


@composite
def valid_password(draw):
    """Generate valid passwords"""
    # Use ASCII characters instead of st.printable
    return draw(st.text(min_size=8, max_size=50, alphabet=st.characters(min_codepoint=32, max_codepoint=126)))


@composite
def valid_book_title(draw):
    """Generate valid book titles"""
    return draw(st.text(min_size=1, max_size=500, alphabet=st.characters(blacklist_categories=('Cc', 'Cs'))))


@composite
def valid_price(draw):
    """Generate valid prices"""
    return draw(st.floats(min_value=0.01, max_value=9999.99, allow_nan=False, allow_infinity=False))


class TestPasswordProperties:
    """Property-based tests for passwords"""
    
    @given(password=valid_password())
    @settings(max_examples=50, deadline=1000)  # Increase deadline for bcrypt
    def test_password_hash_roundtrip(self, password):
        """Property: password hash should verify back"""
        assume(len(password.encode('utf-8')) <= 72)  # bcrypt limitation
        
        hashed = get_password_hash(password)
        
        # Hash properties
        assert hashed != password  # Hash is not equal to original password
        assert len(hashed) > 20     # Hash has reasonable length
        assert verify_password(password, hashed)  # Verification works
    
    @given(password=valid_password(), wrong_password=valid_password())
    @settings(max_examples=30, deadline=1000)  # Increase deadline for bcrypt
    def test_different_passwords_dont_verify(self, password, wrong_password):
        """Property: different passwords should not verify"""
        assume(password != wrong_password)
        assume(len(password.encode('utf-8')) <= 72)
        
        hashed = get_password_hash(password)
        assert not verify_password(wrong_password, hashed)
    
    @given(password=valid_password())
    @settings(max_examples=30, deadline=2000)  # Increase deadline for double hashing
    def test_same_password_different_hashes(self, password):
        """Property: same password should give different hashes (salt)"""
        assume(len(password.encode('utf-8')) <= 72)
        
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)
        
        # Hashes should be different (due to salt)
        assert hash1 != hash2
        # But both should verify
        assert verify_password(password, hash1)
        assert verify_password(password, hash2)


class TestUserModelProperties:
    """Property-based tests for user model"""
    
    @given(
        email=valid_email(),
        username=valid_username(),
        full_name=st.text(max_size=255),
        password=valid_password()
    )
    @settings(max_examples=30, suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=2000)
    def test_user_creation_properties(self, db_session, email, username, full_name, password):
        """Property: user should be created with valid data"""
        assume(len(password.encode('utf-8')) <= 72)
        
        # Add unique prefix to avoid collisions
        import uuid
        unique_suffix = str(uuid.uuid4())[:8]
        unique_email = f"{unique_suffix}_{email}"
        unique_username = f"{unique_suffix}_{username}"
        
        user = User(
            email=unique_email,
            username=unique_username,
            full_name=full_name,
            hashed_password=get_password_hash(password),
            is_active=True
        )
        
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        
        # Properties of created user
        assert user.id is not None
        assert user.email == unique_email
        assert user.username == unique_username
        assert user.full_name == full_name
        assert user.is_active is True
        assert user.is_superuser is False  # Default value
        assert user.created_at is not None
        assert verify_password(password, user.hashed_password)


class TestBookModelProperties:
    """Property-based tests for book model"""
    
    @given(
        title=valid_book_title(),
        description=st.text(max_size=1000),
        price=valid_price(),
        page_count=st.integers(min_value=1, max_value=10000),
        language=st.sampled_from(['en', 'ru', 'fr', 'de', 'es'])
    )
    @settings(max_examples=30, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_book_creation_properties(self, db_session, test_author, test_genre, 
                                    title, description, price, page_count, language):
        """Property: book should be created with valid data"""
        
        book = Book(
            title=title,
            description=description,
            price=price,
            page_count=page_count,
            language=language,
            is_available=True
        )
        book.authors = [test_author]
        book.genres = [test_genre]
        
        db_session.add(book)
        db_session.commit()
        db_session.refresh(book)
        
        # Properties of created book
        assert book.id is not None
        assert book.title == title
        assert book.description == description
        assert book.price == price
        assert book.page_count == page_count
        assert book.language == language
        assert book.is_available is True
        assert book.created_at is not None
        assert len(book.authors) == 1
        assert len(book.genres) == 1
    
    @given(
        title1=valid_book_title(),
        title2=valid_book_title(),
        price1=valid_price(),
        price2=valid_price()
    )
    @settings(max_examples=20, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_book_ordering_properties(self, db_session, test_author, test_genre,
                                    title1, title2, price1, price2):
        """Property: books should sort correctly"""
        assume(title1 != title2)
        
        book1 = Book(title=title1, price=price1, is_available=True)
        book1.authors = [test_author]
        book1.genres = [test_genre]
        
        book2 = Book(title=title2, price=price2, is_available=True)
        book2.authors = [test_author]
        book2.genres = [test_genre]
        
        db_session.add_all([book1, book2])
        db_session.commit()
        
        # Sort by price
        books_by_price = db_session.query(Book).order_by(Book.price).all()
        if price1 < price2:
            assert books_by_price[0].price <= books_by_price[1].price
        
        # Sort by title
        books_by_title = db_session.query(Book).order_by(Book.title).all()
        assert books_by_title[0].title <= books_by_title[1].title


class TestAPISchemaProperties:
    """Property-based tests for API schemas"""
    
    @given(
        title=valid_book_title(),
        price=valid_price(),
        page_count=st.integers(min_value=1, max_value=10000),
        author_ids=st.lists(st.integers(min_value=1, max_value=100), min_size=1, max_size=5),
        genre_ids=st.lists(st.integers(min_value=1, max_value=50), min_size=1, max_size=3)
    )
    @settings(max_examples=20)
    def test_book_create_schema_properties(self, title, price, page_count, author_ids, genre_ids):
        """Property: book creation schema should validate correct data"""
        
        book_data = BookCreate(
            title=title,
            price=price,
            page_count=page_count,
            author_ids=author_ids,
            genre_ids=genre_ids,
            is_available=True
        )
        
        # Properties of valid schema
        assert book_data.title == title
        assert book_data.price == price
        assert book_data.page_count == page_count
        assert len(book_data.author_ids) >= 1
        assert len(book_data.genre_ids) >= 1
        assert book_data.is_available is True
    
    @given(
        email=valid_email(),
        username=valid_username(),
        password=valid_password()
    )
    @settings(max_examples=20)
    def test_user_create_schema_properties(self, email, username, password):
        """Property: user creation schema should validate correct data"""
        
        user_data = UserCreate(
            email=email,
            username=username,
            password=password,
            is_active=True
        )
        
        # Properties of valid schema
        # Email is normalized to lowercase in Pydantic
        assert user_data.email == email.lower()
        assert user_data.username == username
        assert user_data.password == password
        assert user_data.is_active is True


class TestSearchProperties:
    """Property-based tests for search"""
    
    @given(
        search_term=st.text(min_size=1, max_size=50, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd', 'Zs')))
    )
    @settings(max_examples=20, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_search_invariants(self, db_session, test_author, test_genre, search_term):
        """Property: search should maintain invariants"""
        
        # Create books with different titles
        book1 = Book(title=f"Book with {search_term}", is_available=True)
        book1.authors = [test_author]
        book1.genres = [test_genre]
        
        book2 = Book(title="Completely different title", is_available=True)
        book2.authors = [test_author]
        book2.genres = [test_genre]
        
        db_session.add_all([book1, book2])
        db_session.commit()
        
        # Search by term
        search_results = db_session.query(Book).filter(
            Book.title.ilike(f"%{search_term}%")
        ).all()
        
        # Search invariants
        assert len(search_results) <= 2  # No more than all books
        
        # All found books should contain search term
        for book in search_results:
            assert search_term.lower() in book.title.lower()


class TestPaginationProperties:
    """Property-based tests for pagination"""
    
    @given(
        page_size=st.integers(min_value=1, max_value=50),
        total_items=st.integers(min_value=0, max_value=100)
    )
    @settings(max_examples=20)
    def test_pagination_invariants(self, page_size, total_items):
        """Property: pagination should maintain mathematical invariants"""
        
        # Calculate number of pages
        total_pages = (total_items + page_size - 1) // page_size if total_items > 0 else 0
        
        # Pagination invariants
        assert total_pages >= 0
        
        if total_items == 0:
            assert total_pages == 0
        else:
            assert total_pages >= 1
            assert (total_pages - 1) * page_size < total_items <= total_pages * page_size
        
        # Check page sizes
        for page_num in range(1, total_pages + 1):
            offset = (page_num - 1) * page_size
            remaining_items = max(0, total_items - offset)
            page_items = min(page_size, remaining_items)
            
            assert 0 <= page_items <= page_size
            if page_num < total_pages:
                assert page_items == page_size
            else:  # Last page
                assert page_items <= page_size