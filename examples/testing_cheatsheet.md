# 🧪 Python Testing - Master Class

## 🎯 What we created

### 📁 Test Structure

```
tests/
├── __init__.py
├── conftest.py              # Pytest configuration and fixtures
├── test_unit_basic.py       # Unit tests
├── test_api_integration.py  # API integration tests
├── test_property_based.py   # Property-based tests (Hypothesis)
├── test_performance.py      # Performance tests
└── factories.py             # Test data factories
```

### 🔧 Testing Tools

**Main libraries:**
- `pytest` - main testing framework
- `pytest-asyncio` - async test support
- `pytest-cov` - code coverage
- `httpx` - HTTP client for API testing
- `hypothesis` - property-based testing
- `factory-boy` - factories for test data creation
- `faker` - fake data generation

## 🧪 Test Types

### 1. Unit tests
```python
def test_password_hashing():
    """Password hashing test"""
    password = "testpassword123"
    hashed = get_password_hash(password)
    
    assert hashed != password
    assert verify_password(password, hashed)
```

**What we test:**
- Individual functions and methods
- Business logic
- Data validation
- Data models

### 2. Integration tests
```python
def test_create_user(client):
    """User creation test via API"""
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "password123"
    }
    
    response = client.post("/api/v1/users/", json=user_data)
    
    assert response.status_code == 201
    assert response.json()["email"] == user_data["email"]
```

**What we test:**
- API endpoints
- Component interactions
- Authentication and authorization
- CRUD operations

### 3. Property-based tests
```python
@given(password=valid_password())
def test_password_hash_roundtrip(password):
    """Property: password hash should verify back"""
    hashed = get_password_hash(password)
    
    assert hashed != password
    assert verify_password(password, hashed)
```

**What we test:**
- Universal properties
- System invariants
- Edge cases
- Mathematical properties

### 4. Performance tests
```python
def test_search_performance(db_session):
    """Search performance test"""
    create_test_library(db_session, num_books=200)
    
    start_time = time.perf_counter()
    results = db_session.query(Book).filter(
        Book.title.ilike("%test%")
    ).limit(50).all()
    end_time = time.perf_counter()
    
    assert end_time - start_time < 0.05
```

**What we test:**
- Query execution time
- Memory usage
- Concurrent requests
- Scalability

## 🏭 Test Data Factories

### Factory Boy
```python
class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session_persistence = "commit"
    
    email = factory.LazyAttribute(lambda obj: fake.unique.email())
    username = factory.LazyAttribute(lambda obj: fake.unique.user_name())
    full_name = factory.LazyAttribute(lambda obj: fake.name())
```

**Advantages:**
- Automatic data generation
- Object relationships
- Different creation strategies
- Test repeatability

### Faker for realistic data
```python
fake = Faker(['ru_RU', 'en_US'])

name = fake.name()
email = fake.email()
text = fake.text(max_nb_chars=500)
date = fake.date_between(start_date='-1y', end_date='today')
```

## 🔧 Pytest Fixtures

### Basic fixtures
```python
@pytest.fixture
def db_session():
    """Test DB session"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(db_session):
    """Test HTTP client"""
    with TestClient(app) as test_client:
        yield test_client
```

### Data fixtures
```python
@pytest.fixture
def test_user(db_session):
    """Create test user"""
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password=get_password_hash("password123")
    )
    db_session.add(user)
    db_session.commit()
    return user
```

## 📊 Code Coverage

### Configuration
```ini
# pytest.ini
[tool:pytest]
addopts = 
    --cov=bookstore
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=80
```

### Commands
```bash
# Run with coverage
pytest --cov=bookstore

# HTML report
pytest --cov=bookstore --cov-report=html

# Only uncovered lines
pytest --cov=bookstore --cov-report=term-missing
```

## 🚀 Running Tests

### Basic commands
```bash
# All tests
pytest

# Specific file
pytest tests/test_unit_basic.py

# Specific test
pytest tests/test_unit_basic.py::TestPasswordHashing::test_password_hashing

# With verbose output
pytest -v

# In parallel
pytest -n auto

# Only fast tests
pytest -m "not slow"
```

### Markers
```python
@pytest.mark.unit
def test_unit_function():
    pass

@pytest.mark.integration
def test_api_endpoint():
    pass

@pytest.mark.slow
def test_performance():
    pass
```

## 🎯 Best Practices

### Test structure
- ✅ **AAA pattern**: Arrange, Act, Assert
- ✅ **One test = one check**
- ✅ **Descriptive test names**
- ✅ **Test isolation** (each test independent)

### Fixtures
- ✅ **Minimal fixtures** (only necessary data)
- ✅ **Proper scope** (function, class, module, session)
- ✅ **Cleanup** (cleanup after tests)

### Data
- ✅ **Factories instead of hardcode**
- ✅ **Realistic data** (Faker)
- ✅ **Edge cases**

### Property-based tests
- ✅ **Universal properties**
- ✅ **System invariants**
- ✅ **Input constraints** (assume)

## 📈 Quality Metrics

### Code coverage
- **80%+** - good coverage
- **90%+** - excellent coverage
- **100%** - not always necessary

### Coverage types
- **Line coverage** - line coverage
- **Branch coverage** - branch coverage
- **Function coverage** - function coverage

### Performance
- **Unit tests**: < 1ms each
- **Integration tests**: < 100ms each
- **E2E tests**: < 1s each

## 🔍 Test Debugging

### Useful options
```bash
# Stop on first error
pytest -x

# Detailed traceback
pytest --tb=long

# Show print statements
pytest -s

# Run specific test in debugger
pytest --pdb tests/test_unit_basic.py::test_function
```

### Logging in tests
```python
import logging

def test_with_logging(caplog):
    with caplog.at_level(logging.INFO):
        function_that_logs()
    
    assert "Expected message" in caplog.text
```

## 🎉 Result

**In 4 hours we created:**
- ✅ Comprehensive testing system
- ✅ Unit, integration, property-based tests
- ✅ Test data factories
- ✅ Performance tests
- ✅ Pytest configuration with coverage
- ✅ Makefile for automation

**Now you know how to:**
- Write quality tests
- Use modern tools
- Measure code coverage
- Test performance
- Automate testing

**Next step: DevOps + Docker + CI/CD!** 🚀