# 🧪 Complete Guide to Testing Python Applications

## 🎯 What We'll Learn

This guide covers all aspects of modern Python application testing using our BookStore API project as an example.

### 📁 Test Structure

```
tests/
├── __init__.py
├── conftest.py              # pytest configuration and fixtures
├── test_unit_basic.py       # Unit tests for core functionality
├── test_api_integration.py  # API integration tests
├── test_property_based.py   # Property-based tests (Hypothesis)
├── test_performance.py      # Performance tests
├── factories.py             # Test data factories
└── locustfile.py            # Load testing configuration
```

## 🔧 Testing Tools

### Core Libraries
```bash
# Main framework
pytest                 # Modern testing framework
pytest-asyncio         # Async test support
pytest-cov             # Code coverage measurement

# HTTP testing
httpx                  # Modern HTTP client for API testing
requests               # Alternative HTTP client

# Data generation
hypothesis             # Property-based testing
factory-boy            # Factories for creating test objects
faker                  # Realistic fake data generation

# Performance
locust                 # Load testing
pytest-benchmark       # Performance benchmarks
```

## 🧪 Test Types

### 1. Unit Tests - Testing Individual Components

```python
# tests/test_unit_basic.py
import pytest
from bookstore.auth import get_password_hash, verify_password

class TestPasswordHashing:
    """Password hashing system tests"""
    
    def test_password_hashing(self):
        """Test basic password hashing"""
        password = "testpassword123"
        hashed = get_password_hash(password)
        
        # Hash should not match original password
        assert hashed != password
        # Verification should work
        assert verify_password(password, hashed)
    
    def test_different_passwords_different_hashes(self):
        """Different passwords should produce different hashes"""
        password1 = "password1"
        password2 = "password2"
        
        hash1 = get_password_hash(password1)
        hash2 = get_password_hash(password2)
        
        assert hash1 != hash2
    
    def test_wrong_password_verification_fails(self):
        """Wrong password should fail verification"""
        password = "correct_password"
        wrong_password = "wrong_password"
        hashed = get_password_hash(password)
        
        assert not verify_password(wrong_password, hashed)
```

**What we test in Unit tests:**
- ✅ Individual functions and methods
- ✅ Business logic
- ✅ Data validation
- ✅ Data models
- ✅ Utilities and helpers

### 2. Integration Tests - Testing Interactions

```python
# tests/test_api_integration.py
import pytest
from httpx import AsyncClient

class TestUserAPI:
    """User API integration tests"""
    
    async def test_create_user_success(self, client: AsyncClient):
        """Test successful user creation"""
        user_data = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "password123",
            "full_name": "Test User"
        }
        
        response = await client.post("/api/v1/users/", json=user_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == user_data["email"]
        assert data["username"] == user_data["username"]
        assert "password" not in data  # Password should not be returned
    
    async def test_create_user_duplicate_email(self, client: AsyncClient, test_user):
        """Test creating user with duplicate email"""
        user_data = {
            "email": test_user.email,  # Use existing email
            "username": "newuser",
            "password": "password123"
        }
        
        response = await client.post("/api/v1/users/", json=user_data)
        
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"]
    
    async def test_login_success(self, client: AsyncClient, test_user):
        """Test successful login"""
        login_data = {
            "username": test_user.email,
            "password": "password123"
        }
        
        response = await client.post("/auth/login", data=login_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
```

**What we test in integration tests:**
- ✅ API endpoints
- ✅ Authentication and authorization
- ✅ CRUD operations
- ✅ Database interactions
- ✅ Input data validation
- ✅ Error handling

### 3. Property-based Tests - Testing Properties

```python
# tests/test_property_based.py
import pytest
from hypothesis import given, strategies as st, assume
from bookstore.auth import get_password_hash, verify_password

class TestPasswordProperties:
    """Property-based tests for password system"""
    
    @given(password=st.text(min_size=1, max_size=100))
    def test_password_hash_roundtrip(self, password):
        """Property: password hash should verify back"""
        # Exclude empty strings and whitespace-only strings
        assume(password.strip())
        
        hashed = get_password_hash(password)
        
        # Core properties
        assert hashed != password  # Hash differs from original
        assert verify_password(password, hashed)  # Verification works
        assert len(hashed) > 0  # Hash is not empty
    
    @given(
        password1=st.text(min_size=1, max_size=50),
        password2=st.text(min_size=1, max_size=50)
    )
    def test_different_passwords_different_hashes(self, password1, password2):
        """Property: different passwords produce different hashes"""
        assume(password1 != password2)
        assume(password1.strip() and password2.strip())
        
        hash1 = get_password_hash(password1)
        hash2 = get_password_hash(password2)
        
        assert hash1 != hash2

# Custom strategies for data generation
@st.composite
def valid_email(draw):
    """Generator for valid email addresses"""
    username = draw(st.text(
        alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd')),
        min_size=1, max_size=20
    ))
    domain = draw(st.sampled_from(['example.com', 'test.org', 'demo.net']))
    return f"{username}@{domain}"

@st.composite
def valid_book_data(draw):
    """Generator for book data"""
    return {
        "title": draw(st.text(min_size=1, max_size=200)),
        "description": draw(st.text(max_size=1000)),
        "price": draw(st.floats(min_value=0, max_value=10000, allow_nan=False)),
        "isbn": draw(st.text(min_size=10, max_size=13, alphabet=st.characters(whitelist_categories=('Nd',))))
    }
```

**What we test in property-based tests:**
- ✅ Universal system properties
- ✅ Invariants (what should remain unchanged)
- ✅ Edge cases
- ✅ Mathematical properties
- ✅ Round-trip operations (serialization/deserialization)

### 4. Performance Tests

```python
# tests/test_performance.py
import time
import pytest
from httpx import AsyncClient

class TestPerformance:
    """API performance tests"""
    
    async def test_book_search_performance(self, client: AsyncClient, sample_books):
        """Test book search performance"""
        # Create test data
        await self.create_test_books(client, count=100)
        
        # Measure search time
        start_time = time.perf_counter()
        
        response = await client.get("/api/v1/books/?q=test&limit=20")
        
        end_time = time.perf_counter()
        duration = end_time - start_time
        
        # Check result and performance
        assert response.status_code == 200
        assert duration < 0.1  # Search should take less than 100ms
        
        data = response.json()
        assert len(data["items"]) <= 20
    
    async def test_concurrent_requests(self, client: AsyncClient):
        """Test concurrent requests"""
        import asyncio
        
        async def make_request():
            response = await client.get("/api/v1/books/")
            return response.status_code
        
        # Run 10 parallel requests
        start_time = time.perf_counter()
        
        tasks = [make_request() for _ in range(10)]
        results = await asyncio.gather(*tasks)
        
        end_time = time.perf_counter()
        duration = end_time - start_time
        
        # All requests should be successful
        assert all(status == 200 for status in results)
        # Parallel requests shouldn't take too long
        assert duration < 1.0
    
    @pytest.mark.benchmark
    def test_password_hashing_benchmark(self, benchmark):
        """Password hashing benchmark"""
        password = "test_password_123"
        
        # Measure hashing performance
        result = benchmark(get_password_hash, password)
        
        assert len(result) > 0
        assert result != password
```

## 🏭 Test Data Factories

### Factory Boy for Object Creation

```python
# tests/factories.py
import factory
from factory.alchemy import SQLAlchemyModelFactory
from faker import Faker
from bookstore.models import User, Book, Author, Genre
from bookstore.database import SessionLocal

fake = Faker(['ru_RU', 'en_US'])

class UserFactory(SQLAlchemyModelFactory):
    """Factory for creating users"""
    
    class Meta:
        model = User
        sqlalchemy_session_persistence = "commit"
    
    email = factory.LazyAttribute(lambda obj: fake.unique.email())
    username = factory.LazyAttribute(lambda obj: fake.unique.user_name())
    full_name = factory.LazyAttribute(lambda obj: fake.name())
    hashed_password = factory.LazyAttribute(
        lambda obj: get_password_hash("password123")
    )
    is_active = True
    is_superuser = False

class AuthorFactory(SQLAlchemyModelFactory):
    """Factory for creating authors"""
    
    class Meta:
        model = Author
        sqlalchemy_session_persistence = "commit"
    
    name = factory.LazyAttribute(lambda obj: fake.name())
    biography = factory.LazyAttribute(lambda obj: fake.text(max_nb_chars=500))
    birth_date = factory.LazyAttribute(
        lambda obj: fake.date_between(start_date='-100y', end_date='-20y')
    )

class BookFactory(SQLAlchemyModelFactory):
    """Factory for creating books"""
    
    class Meta:
        model = Book
        sqlalchemy_session_persistence = "commit"
    
    title = factory.LazyAttribute(lambda obj: fake.sentence(nb_words=4)[:-1])
    description = factory.LazyAttribute(lambda obj: fake.text(max_nb_chars=1000))
    price = factory.LazyAttribute(lambda obj: fake.pydecimal(
        left_digits=3, right_digits=2, positive=True, min_value=1, max_value=999
    ))
    isbn = factory.LazyAttribute(lambda obj: fake.isbn13())
    publication_date = factory.LazyAttribute(
        lambda obj: fake.date_between(start_date='-50y', end_date='today')
    )
    
    # Many-to-many relationships
    @factory.post_generation
    def authors(self, create, extracted, **kwargs):
        if not create:
            return
        
        if extracted:
            for author in extracted:
                self.authors.append(author)
        else:
            # Create random author
            author = AuthorFactory()
            self.authors.append(author)

# Using factories in tests
def test_user_creation():
    """Example of using factory"""
    user = UserFactory()
    assert user.email
    assert user.username
    assert user.hashed_password

def test_book_with_authors():
    """Creating book with authors"""
    authors = AuthorFactory.create_batch(2)
    book = BookFactory(authors=authors)
    
    assert len(book.authors) == 2
    assert book.title
    assert book.price > 0
```

### Faker for Realistic Data

```python
from faker import Faker

# Support for Russian and English languages
fake = Faker(['ru_RU', 'en_US'])

# Data generation examples
name = fake.name()                    # "John Doe"
email = fake.email()                  # "john@example.com"
text = fake.text(max_nb_chars=500)    # Random text
date = fake.date_between(start_date='-1y', end_date='today')
phone = fake.phone_number()           # Phone number
address = fake.address()              # Address
company = fake.company()              # Company name
isbn = fake.isbn13()                  # Book ISBN
price = fake.pydecimal(left_digits=3, right_digits=2, positive=True)
```

## 🔧 pytest Configuration

### conftest.py - Central Configuration

```python
# tests/conftest.py
import pytest
import asyncio
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bookstore.main import app
from bookstore.database import get_db, Base
from bookstore.config import get_settings

# Testing settings
settings = get_settings()
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for entire test session"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def db_session():
    """Fixture for working with test database"""
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Clean tables after each test
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
async def client(db_session):
    """HTTP client fixture for API testing"""
    
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(app=app, base_url="http://test") as test_client:
        yield test_client
    
    app.dependency_overrides.clear()

@pytest.fixture
def test_user(db_session):
    """Fixture for creating test user"""
    from tests.factories import UserFactory
    UserFactory._meta.sqlalchemy_session = db_session
    return UserFactory()

@pytest.fixture
def admin_user(db_session):
    """Fixture for creating admin user"""
    from tests.factories import UserFactory
    UserFactory._meta.sqlalchemy_session = db_session
    return UserFactory(is_superuser=True)

@pytest.fixture
async def authenticated_client(client: AsyncClient, test_user):
    """Authenticated client fixture"""
    # Get token
    login_data = {
        "username": test_user.email,
        "password": "password123"
    }
    response = await client.post("/auth/login", data=login_data)
    token = response.json()["access_token"]
    
    # Add token to headers
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client
```

### pytest.ini - pytest Configuration

```ini
# pytest.ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

# Markers for test categorization
markers =
    unit: Unit tests
    integration: Integration tests
    property: Property-based tests
    performance: Performance tests
    slow: Slow tests that take more than 1 second

# Code coverage settings
addopts = 
    --cov=bookstore
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=80
    --strict-markers
    -v

# Async tests
asyncio_mode = auto

# Warning filters
filterwarnings =
    ignore::DeprecationWarning
    ignore::PendingDeprecationWarning
```

## 📊 Code Coverage Measurement

### Coverage Commands

```bash
# Run tests with coverage
pytest --cov=bookstore

# HTML report (creates htmlcov/ folder)
pytest --cov=bookstore --cov-report=html

# Show uncovered lines
pytest --cov=bookstore --cov-report=term-missing

# Set minimum coverage threshold
pytest --cov=bookstore --cov-fail-under=90

# Coverage for changed files only
pytest --cov=bookstore --cov-report=term-missing --cov-branch
```

### Coverage Configuration (.coveragerc)

```ini
# .coveragerc
[run]
source = bookstore
omit = 
    */tests/*
    */venv/*
    */migrations/*
    */conftest.py
    */settings/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:

[html]
directory = htmlcov
```

## 🚀 Running Tests

### Basic Commands

```bash
# All tests
pytest

# Specific file
pytest tests/test_unit_basic.py

# Specific test
pytest tests/test_unit_basic.py::TestPasswordHashing::test_password_hashing

# Tests by markers
pytest -m unit                    # Unit tests only
pytest -m "not slow"              # Exclude slow tests
pytest -m "unit or integration"   # Unit or integration tests

# Parallel execution
pytest -n auto                    # Automatic process count
pytest -n 4                       # 4 processes

# Verbose output
pytest -v                         # Verbose
pytest -s                         # Show print statements
pytest --tb=short                 # Short traceback

# Stop on first failure
pytest -x

# Re-run failed tests only
pytest --lf                       # Last failed
pytest --ff                       # Failed first
```

### Makefile Commands

```makefile
# Makefile
test:
	pytest

test-unit:
	pytest -m unit

test-integration:
	pytest -m integration

test-property:
	pytest -m property --hypothesis-show-statistics

test-performance:
	pytest -m performance

test-coverage:
	pytest --cov=bookstore --cov-report=html --cov-report=term-missing

test-fast:
	pytest -m "not slow" -x

test-parallel:
	pytest -n auto
```

## 🎯 Testing Best Practices

### Test Structure (AAA Pattern)

```python
def test_user_creation():
    # Arrange (Setup)
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "password123"
    }
    
    # Act (Action)
    user = create_user(user_data)
    
    # Assert (Verification)
    assert user.email == user_data["email"]
    assert user.username == user_data["username"]
    assert user.id is not None
```

### Test Naming

```python
# ✅ Good - descriptive names
def test_user_creation_with_valid_data_succeeds():
    pass

def test_user_creation_with_duplicate_email_fails():
    pass

def test_password_hashing_produces_different_hash_each_time():
    pass

# ❌ Bad - non-descriptive names
def test_user():
    pass

def test_create():
    pass

def test_password():
    pass
```

### Test Isolation

```python
# ✅ Good - each test is independent
class TestUserService:
    def test_create_user(self, db_session):
        user = UserFactory()
        assert user.id is not None
    
    def test_get_user_by_id(self, db_session):
        user = UserFactory()
        found_user = get_user_by_id(db_session, user.id)
        assert found_user.id == user.id

# ❌ Bad - tests depend on each other
class TestUserService:
    def test_create_user(self, db_session):
        self.user = UserFactory()  # Save in self
    
    def test_get_user_by_id(self, db_session):
        # Depends on previous test
        found_user = get_user_by_id(db_session, self.user.id)
```

### Using Fixtures

```python
# ✅ Good - minimal fixtures
@pytest.fixture
def user_data():
    """Basic user data"""
    return {
        "email": "test@example.com",
        "username": "testuser",
        "password": "password123"
    }

@pytest.fixture
def test_user(db_session, user_data):
    """Created user in database"""
    return UserFactory(**user_data)

# ❌ Bad - excessive fixtures
@pytest.fixture
def everything_fixture(db_session):
    """Creates all possible objects"""
    users = UserFactory.create_batch(10)
    books = BookFactory.create_batch(50)
    authors = AuthorFactory.create_batch(20)
    # ... lots of unnecessary data
    return {
        'users': users,
        'books': books,
        'authors': authors
    }
```

## 📈 Test Quality Metrics

### Code Coverage
- **80%+** - good coverage
- **90%+** - excellent coverage  
- **95%+** - outstanding coverage
- **100%** - not always necessary

### Coverage Types
- **Line coverage** - line coverage
- **Branch coverage** - branch coverage (if/else)
- **Function coverage** - function coverage
- **Condition coverage** - condition coverage

### Test Performance
- **Unit tests**: < 1ms each
- **Integration tests**: < 100ms each
- **E2E tests**: < 1s each
- **Total time**: < 5 minutes for entire suite

### Reliability
- **Flaky tests**: < 1% (unstable tests)
- **False positives**: minimum
- **False negatives**: unacceptable

## 🔍 Debugging and Diagnostics

### Useful pytest Options

```bash
# Stop on first failure
pytest -x

# Verbose traceback
pytest --tb=long

# Show print statements
pytest -s

# Run in debugger
pytest --pdb

# Profile tests
pytest --durations=10

# Show slowest tests
pytest --durations=0
```

### Logging in Tests

```python
import logging

def test_with_logging(caplog):
    """Test with log checking"""
    with caplog.at_level(logging.INFO):
        function_that_logs_info()
    
    assert "Expected log message" in caplog.text
    assert caplog.records[0].levelname == "INFO"

def test_with_custom_logger(caplog):
    """Test with custom logger"""
    logger = logging.getLogger("bookstore.auth")
    
    with caplog.at_level(logging.DEBUG, logger="bookstore.auth"):
        logger.debug("Debug message")
    
    assert "Debug message" in caplog.text
```

## 🎉 Conclusion

### What We Learned

**Testing Types:**
- ✅ Unit tests for individual components
- ✅ Integration tests for API
- ✅ Property-based tests for universal properties
- ✅ Performance tests

**Tools:**
- ✅ pytest as main framework
- ✅ Factory Boy for test data creation
- ✅ Hypothesis for property-based testing
- ✅ httpx for API testing

**Best Practices:**
- ✅ AAA pattern (Arrange, Act, Assert)
- ✅ Test isolation
- ✅ Descriptive names
- ✅ Minimal fixtures
- ✅ Code coverage measurement

**Automation:**
- ✅ Configuration through pytest.ini
- ✅ Makefile for convenience
- ✅ CI/CD integration

### Next Steps

1. **Practice**: Write tests for your project
2. **CI/CD**: Integrate tests into pipeline
3. **Monitoring**: Track quality metrics
4. **Team Training**: Share knowledge

**Remember**: Good tests are an investment in your project's future! 🚀