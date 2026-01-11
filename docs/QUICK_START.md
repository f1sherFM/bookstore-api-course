# 🚀 Quick Start - BookStore API

## 🎯 What is this?

BookStore API is a modern, production-ready book management system built using Python development and DevOps best practices.

### ⚡ Key Features

- **FastAPI** - modern, fast web framework
- **JWT Authentication** - secure authorization system
- **SQLAlchemy ORM** - database operations
- **Comprehensive Testing** - 95%+ code coverage
- **Docker Containerization** - easy deployment
- **Kubernetes Support** - scalability
- **Monitoring** - Prometheus + Grafana
- **CI/CD Pipeline** - automation

## 🏃‍♂️ Quick Launch (3 minutes)

### Option 1: One Script (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd bookstore-api

# Run setup script
./scripts/setup-dev.sh

# Start development server
make dev
```

### Option 2: Docker (Easiest)

```bash
# Launch all services with Docker
make docker-dev

# API available at: http://localhost:8000
# Documentation: http://localhost:8000/docs
```

### Option 3: Manual Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r fastapi_requirements.txt

# Setup environment
cp .env.example .env

# Run tests
pytest

# Start server
python run_bookstore.py
```

## 📖 First Steps

### 1. Open API Documentation

Navigate to: http://localhost:8000/docs

Here you'll find:
- ✅ Interactive documentation for all endpoints
- ✅ Ability to test API directly in browser
- ✅ Data schemas and request examples

### 2. Create First User

```bash
# POST /api/v1/users/
curl -X POST "http://localhost:8000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "username": "admin",
    "password": "admin123",
    "full_name": "Administrator",
    "is_superuser": true
  }'
```

### 3. Login to System

```bash
# POST /auth/login
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@example.com&password=admin123"
```

Save the received `access_token` for further requests.

### 4. Create First Book

```bash
# POST /api/v1/books/
curl -X POST "http://localhost:8000/api/v1/books/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "title": "War and Peace",
    "description": "Epic novel by Leo Tolstoy",
    "price": 599.99,
    "isbn": "9785170123456"
  }'
```

## 🔧 Main Commands

### Development

```bash
make dev              # Start development server
make test             # Run all tests
make test-coverage    # Tests with code coverage
make lint             # Check code with linters
make format           # Format code
```

### Docker

```bash
make docker-build     # Build Docker image
make docker-dev       # Start development environment
make docker-prod      # Start production environment
make logs             # Show application logs
```

### Testing

```bash
make test-unit        # Unit tests
make test-integration # Integration tests
make test-property    # Property-based tests
make test-performance # Performance tests
```

### Security

```bash
make security-scan    # Security scanning
make health           # Check application health
```

## 📊 API Structure

### 🔐 Authentication

```
POST /auth/login      # Login to system
GET  /auth/me         # Current user information
```

### 📚 Book Management

```
GET    /api/v1/books/           # List books (search, filters)
POST   /api/v1/books/           # Create book (admin)
GET    /api/v1/books/{id}       # Book details
PUT    /api/v1/books/{id}       # Update book (admin)
DELETE /api/v1/books/{id}       # Delete book (admin)
GET    /api/v1/books/stats      # Book statistics
```

### 👥 Users

```
GET    /api/v1/users/           # List users (admin)
POST   /api/v1/users/           # Registration
GET    /api/v1/users/{id}       # User profile
PUT    /api/v1/users/{id}       # Update profile
DELETE /api/v1/users/{id}       # Delete user (admin)
```

### ⭐ Reviews

```
GET    /api/v1/reviews/         # List reviews
POST   /api/v1/reviews/         # Create review
PUT    /api/v1/reviews/{id}     # Update review
DELETE /api/v1/reviews/{id}     # Delete review
```

### 📖 Reading Lists

```
GET    /api/v1/reading-lists/           # My lists
GET    /api/v1/reading-lists/public     # Public lists
POST   /api/v1/reading-lists/           # Create list
POST   /api/v1/reading-lists/{id}/books # Add book
DELETE /api/v1/reading-lists/{id}/books/{book_id} # Remove book
```

### 🏥 System Endpoints

```
GET /health           # Health check
GET /metrics          # Prometheus metrics
GET /info             # Application information
```

## 🎓 Learning Materials

### Documentation

- **[Project Structure](docs/PROJECT_STRUCTURE_DETAILED.md)** - Detailed architecture overview
- **[Testing Guide](docs/TESTING_GUIDE.md)** - All about testing
- **[Docker & DevOps](docs/DOCKER_DEVOPS_GUIDE.md)** - Deployment and monitoring

### Code Examples

- **[FastAPI Examples](examples/fastapi_cheatsheet.md)** - Learning FastAPI
- **[Testing Examples](examples/testing_cheatsheet.md)** - Testing best practices
- **[OOP Examples](examples/oop_cheatsheet.md)** - Object-oriented programming

## 🚀 Deployment Options

### Local Development

```bash
make dev
# Available at: http://localhost:8000
```

### Docker Development

```bash
make docker-dev
# Full stack with database and cache
```

### Production Deployment

```bash
make deploy-prod
# SSL, monitoring, backup
```

### Kubernetes

```bash
make k8s-deploy
# Auto-scaling, high availability
```

## 🔍 Monitoring and Debugging

### Application Logs

```bash
make logs              # Docker logs
tail -f logs/app.log   # File logs
```

### Metrics

```bash
curl http://localhost:8000/metrics  # Prometheus metrics
make health                         # Health check
```

### Dashboards

- **Grafana**: http://localhost:3000 (admin/admin)
- **Prometheus**: http://localhost:9090

## ❓ Frequently Asked Questions

### Q: How to change application port?

A: Edit the `PORT` variable in `.env` file or `run_bookstore.py`

### Q: How to add new endpoint?

A: 
1. Create new router in `bookstore/routers/`
2. Add it to `bookstore/main.py`
3. Write tests in `tests/`

### Q: How to configure database?

A: Edit `DATABASE_URL` in `.env` file

### Q: How to run only tests?

A: `make test` or `pytest tests/`

### Q: How to deploy to production?

A: Follow instructions in `docs/PRODUCTION_DEPLOYMENT.md`

## 🆘 Getting Help

### Documentation

- Check `docs/` folder for detailed guides
- Study examples in `examples/` folder
- Read code comments

### Debugging

```bash
# Check logs
make logs

# Check health
make health

# Run diagnostics
./scripts/production-health-check.sh
```

### Community

- Create Issue on GitHub
- Check existing Issues
- Read CONTRIBUTING.md

## 🎉 Congratulations!

Now you have a fully functional, production-ready API! 

**Next Steps:**
1. Study API documentation at `/docs`
2. Run tests: `make test`
3. Try creating books and users
4. Explore monitoring and logs
5. Deploy to production

**Happy coding! 🚀**