# 🎓 BookStore API - Complete Modern Python Development Course

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Master-green.svg)
![Docker](https://img.shields.io/badge/Docker-DevOps-blue.svg)
![Tests](https://img.shields.io/badge/Testing-95%25-brightgreen.svg)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Production-orange.svg)

**Comprehensive educational project: from Python basics to production-ready system**

[🚀 Quick Start](#-quick-start) • [📚 Learning Materials](#-learning-materials) • [🎯 Curriculum](#-curriculum) • [💡 Code Examples](#-code-examples)

</div>

---

## 🌟 About the Project

This project represents a **complete modern Python development course** that will take you from basic concepts to creating a production-ready system with a full DevOps pipeline.

### 🎯 What You'll Learn

- ⚡ **Modern Python** - async/await, type hints, decorators
- 🌐 **FastAPI Development** - REST API, authentication, documentation
- 🧪 **Comprehensive Testing** - unit, integration, property-based tests
- 🐳 **Docker Containerization** - from development to production
- ☸️ **Kubernetes Orchestration** - auto-scaling, monitoring
- 📊 **DevOps Practices** - CI/CD, monitoring, security

### 🏆 Learning Outcomes

After completing the course, you'll be able to:
- 🚀 Create production-ready API applications
- 🧪 Write quality tests with high coverage
- 🐳 Containerize and deploy applications
- 📊 Set up monitoring and logging
- 🔒 Ensure security at all levels

---

## 🚀 Quick Start

### Launch in 3 Minutes

```bash
# 1. Clone the project
git clone <repository-url>
cd bookstore-api

# 2. Run automatic setup
./scripts/setup-dev.sh

# 3. Start the server
make dev

# 4. Open documentation
# http://localhost:8000/docs
```

### Alternative Docker Launch

```bash
# Launch full stack with one command
make docker-dev

# API: http://localhost:8000
# Documentation: http://localhost:8000/docs
# Monitoring: http://localhost:3000
```

---

## 📚 Learning Materials

### 🎓 Main Guides

| 📖 Document | 📝 Description | ⏱️ Time | 🎯 Level |
|-------------|-------------|----------|------------|
| **[Quick Start](docs/QUICK_START.md)** | Project launch and first steps | 30 min | 🟢 Beginner |
| **[Project Structure](docs/PROJECT_STRUCTURE_DETAILED.md)** | Architecture and code organization | 1 hour | 🟡 Intermediate |
| **[Testing Guide](docs/TESTING_GUIDE.md)** | All types of Python testing | 3 hours | 🟠 Advanced |
| **[Docker & DevOps](docs/DOCKER_DEVOPS_GUIDE.md)** | Containerization and deployment | 4 hours | 🔴 Expert |
| **[Learning Materials](docs/LEARNING_MATERIALS.md)** | Complete curriculum | 2 weeks | 🎓 Course |

### 💡 Practical Examples

| 🔧 File | 🎯 Topic | 📋 What You'll Learn |
|---------|---------|-----------------|
| **[FastAPI Cheatsheet](examples/fastapi_cheatsheet.md)** | Web Development | REST API, JWT, documentation |
| **[Testing Cheatsheet](examples/testing_cheatsheet.md)** | Code Quality | pytest, coverage, property-based |
| **[OOP Cheatsheet](examples/oop_cheatsheet.md)** | Python Basics | Classes, inheritance, polymorphism |
| **[Decorators & Types](examples/decorators_typehints_cheatsheet.md)** | Advanced Python | Decorators, type hints, Generic |

---

## 🎯 Curriculum

### 📅 Structured Learning

#### 🟢 Week 1: Python Basics and FastAPI

**Days 1-2: Python Fundamentals**
- 📖 Study [OOP Cheatsheet](examples/oop_cheatsheet.md)
- 💻 Launch project with [Quick Start](docs/QUICK_START.md)
- 🔧 Study code in `bookstore/models.py` and `bookstore/schemas.py`

**Days 3-5: FastAPI Development**
- 📖 Study [FastAPI Cheatsheet](examples/fastapi_cheatsheet.md)
- 💻 Create new endpoint for genres
- 🔧 Add validation with Pydantic

**Practical Assignment:**
- ✅ Create API for book authors management
- ✅ Add search and filtering
- ✅ Set up JWT authentication

#### 🟡 Week 2: Testing and Code Quality

**Days 1-3: Testing Basics**
- 📖 Study [Testing Guide](docs/TESTING_GUIDE.md)
- 💻 Run existing tests: `make test`
- 🔧 Study code in `tests/`

**Days 4-7: Advanced Testing**
- 📖 Study [Testing Cheatsheet](examples/testing_cheatsheet.md)
- 💻 Write unit tests for new functionality
- 🔧 Create property-based tests

**Practical Assignment:**
- ✅ Achieve 95%+ code coverage
- ✅ Write integration tests for API
- ✅ Create load tests with Locust

#### 🟠 Week 3: Docker and Containerization

**Days 1-4: Docker Basics**
- 📖 Study [Docker Guide](docs/DOCKER_DEVOPS_GUIDE.md)
- 💻 Build Docker image: `make docker-build`
- 🔧 Run production stack: `make docker-prod`

**Days 5-7: Production Deployment**
- 💻 Set up monitoring with Prometheus and Grafana
- 🔧 Study configurations in `docker-compose.prod.yml`

**Practical Assignment:**
- ✅ Create optimized Dockerfile
- ✅ Set up production environment
- ✅ Add health checks and monitoring

#### 🔴 Week 4: Kubernetes and DevOps

**Days 1-4: Kubernetes**
- 📖 Continue [Docker Guide](docs/DOCKER_DEVOPS_GUIDE.md)
- 💻 Deploy to Kubernetes: `make k8s-deploy`
- 🔧 Study manifests in `k8s/`

**Days 5-7: CI/CD and Automation**
- 💻 Set up GitHub Actions pipeline
- 🔧 Study workflows in `.github/workflows/`

**Practical Assignment:**
- ✅ Create Kubernetes deployment with auto-scaling
- ✅ Set up CI/CD pipeline
- ✅ Add automated security tests

---

## 💻 Practical Assignments

### 🎯 Level-Based Tasks

#### 🟢 Level 1: Basics (1-2 days)

**Goal:** Understand project structure and launch API

**Tasks:**
1. ✅ Launch project locally
2. ✅ Create 5 books through Swagger UI
3. ✅ Register user and log in
4. ✅ Study code structure in `bookstore/`

**Success Criteria:**
- API starts without errors
- Can create and retrieve data
- Understand basic architecture

#### 🟡 Level 2: Web Development (3-5 days)

**Goal:** Create new API functionality

**Tasks:**
1. ✅ Create model and API for book genres
2. ✅ Add book search by author and genre
3. ✅ Implement pagination for all lists
4. ✅ Add data validation with custom rules

**Success Criteria:**
- New endpoints work correctly
- Validation rejects incorrect data
- Documentation updates automatically

#### 🟠 Level 3: Testing (5-7 days)

**Goal:** Ensure code quality with tests

**Tasks:**
1. ✅ Write 20+ unit tests for business logic
2. ✅ Create integration tests for all APIs
3. ✅ Add property-based tests with Hypothesis
4. ✅ Achieve 95%+ code coverage

**Success Criteria:**
- All tests pass successfully
- Code coverage above 95%
- Tests find real bugs

#### 🔴 Level 4: DevOps (7-10 days)

**Goal:** Deploy production-ready system

**Tasks:**
1. ✅ Build optimized Docker image
2. ✅ Set up production environment with monitoring
3. ✅ Create Kubernetes deployment
4. ✅ Set up CI/CD pipeline with automated tests

**Success Criteria:**
- Application works in production
- Monitoring shows metrics
- CI/CD automatically deploys changes

---

## 🛠️ Technology Stack

### 🐍 Backend Development

```python
# Core Technologies
FastAPI      # Modern web framework
SQLAlchemy   # ORM for database work
Pydantic     # Data validation
JWT          # Authentication
bcrypt       # Password hashing
```

### 🧪 Testing

```python
# Testing Frameworks
pytest       # Main framework
httpx        # HTTP client for API tests
hypothesis   # Property-based testing
locust       # Load testing
factory-boy  # Test data factories
```

### 🐳 DevOps Tools

```yaml
# Containerization and Orchestration
Docker       # Containerization
Kubernetes   # Orchestration
Nginx        # Web server and load balancer

# Monitoring
Prometheus   # Metrics collection
Grafana      # Visualization
Loki         # Log aggregation
```

---

## 📊 Learning Progress

### ✅ Skills Checklist

**Python Development:**
- [ ] Understand async/await programming
- [ ] Use type hints for static typing
- [ ] Create decorators and understand metaprogramming
- [ ] Apply OOP principles in real projects

**Web Development:**
- [ ] Create REST API with FastAPI
- [ ] Set up JWT authentication
- [ ] Validate data with Pydantic
- [ ] Document API with OpenAPI/Swagger

**Testing:**
- [ ] Write unit tests with pytest
- [ ] Create integration tests for API
- [ ] Use property-based testing
- [ ] Measure and analyze code coverage

**DevOps:**
- [ ] Containerize applications with Docker
- [ ] Deploy to Kubernetes
- [ ] Set up CI/CD pipelines
- [ ] Monitor applications in production

### 🏆 Certification

**Get course completion certificate:**

1. ✅ Complete all practical assignments
2. ✅ Create your own project based on what you learned
3. ✅ Demonstrate working production system
4. ✅ Share results with community

---

## 🎉 Community and Support

### 💬 Getting Help

**Documentation:**
- 📖 Check relevant guides
- 💡 Study code examples
- 🔍 Use documentation search

**Practical Help:**
```bash
make help     # List all commands
make health   # Check system status
make logs     # View application logs
```

**Community:**
- 🐛 Create Issues for questions
- 💡 Suggest improvements
- 🤝 Help other participants

### 🌟 Share Success

**After completing the course:**
- ⭐ Star the project on GitHub
- 📝 Write course review
- 🚀 Share your project
- 👥 Help other learners

---

## 🚀 Next Steps

### 🎯 After Course Completion

**Apply Knowledge:**
1. 💼 Create portfolio project
2. 🏢 Apply skills at work
3. 🌐 Participate in open source projects
4. 📚 Study advanced topics

**Career Opportunities:**
- 🐍 **Python Backend Developer**
- 🌐 **API Developer**
- 🧪 **QA Automation Engineer**
- 🐳 **DevOps Engineer**
- ☸️ **Kubernetes Administrator**

### 📈 Advanced Topics

**For further study:**
- 🔄 Microservices architecture
- 🤖 Machine learning and MLOps
- 🔒 Advanced security
- 📊 Big Data and analytics
- 🌩️ Serverless architectures

---

<div align="center">

## 🎓 Start Your Journey into Modern Development!

**From Beginner to Expert in 4 Weeks**

[🚀 Start Learning](docs/QUICK_START.md) • [📚 Learning Materials](docs/LEARNING_MATERIALS.md) • [💻 Code Examples](examples/)

---

**Created with ❤️ for modern Python development learners**

*This project is the result of 2 days of intensive development and years of experience creating production systems*

</div>