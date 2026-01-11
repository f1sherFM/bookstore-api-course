# 🚀 CI/CD Setup for BookStore API

## Overview

Complete CI/CD pipeline automation using GitHub Actions for testing, building, security scanning, and deployment of BookStore API.

## Workflow Structure

```
.github/workflows/
├── ci.yml              # Main CI/CD pipeline
├── dependencies.yml    # Dependency management
└── performance.yml     # Performance testing
```

## Main CI/CD Pipeline (ci.yml)

### Pipeline Stages

1. **Test** - Testing and linting
2. **Security** - Security scanning
3. **Build** - Docker image building
4. **Deploy Staging** - Staging deployment
5. **Deploy Production** - Production deployment
6. **Notify** - Result notifications

### Triggers

```yaml
on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
```

### Stage 1: Testing

```yaml
services:
  postgres:
    image: postgres:15
  redis:
    image: redis:7-alpine

steps:
  - Checkout code
  - Set up Python 3.11
  - Install dependencies
  - Run linting (black, isort, flake8, mypy)
  - Run unit tests
  - Run integration tests
  - Run property-based tests
  - Run performance tests
  - Generate coverage report
```

**Code quality tools:**
- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Code linting
- **mypy**: Type checking
- **pytest**: Testing
- **coverage**: Code coverage

### Stage 2: Security Scanning

```yaml
steps:
  - safety check (dependencies)
  - bandit (Python code)
  - semgrep (static analysis)
  - Upload security reports
```

**Security tools:**
- **Safety**: Vulnerability checking in dependencies
- **Bandit**: Security issue detection in code
- **Semgrep**: Static security analysis

### Stage 3: Docker Build

```yaml
steps:
  - Multi-platform build (amd64, arm64)
  - Push to GitHub Container Registry
  - Generate SBOM (Software Bill of Materials)
  - Cache optimization
```

**Docker features:**
- Multi-stage build for optimization
- Multi-platform support
- Layer caching for acceleration
- SBOM for component tracking

### Stage 4: Deployment

#### Staging (automatic)
- Trigger: push to `develop` branch
- Automatic deployment
- Smoke tests
- Notifications

#### Production (with approval)
- Trigger: push to `main` branch
- Requires manual approval
- Blue-green deployment
- Health checks
- Release creation

## Dependency Management (dependencies.yml)

### Automatic Updates

```yaml
schedule:
  - cron: '0 9 * * 1'  # Every Monday at 9:00
```

**Features:**
- Python dependency updates
- Security scanning
- Pull Request creation with updates
- License checking

### Tools

- **pip-tools**: Dependency management
- **safety**: Vulnerability checking
- **Trivy**: Docker image scanning
- **Snyk**: Additional security scanning

## Performance Testing (performance.yml)

### Load Testing

```yaml
schedule:
  - cron: '0 2 * * *'  # Every day at 2:00
```

**Capabilities:**
- Load testing with Locust
- Uptime monitoring
- Metrics analysis
- Performance reports

### Locust Configuration

```python
class BookStoreUser(HttpUser):
    wait_time = between(1, 3)
    
    @task(3)
    def view_books(self):
        self.client.get("/api/v1/books/")
    
    @task(2)
    def view_book_details(self):
        book_id = random.randint(1, 10)
        self.client.get(f"/api/v1/books/{book_id}")
```

## Project Configuration

### pyproject.toml

```toml
[tool.black]
line-length = 127
target-version = ['py311']

[tool.isort]
profile = "black"
line-length = 127

[tool.mypy]
python_version = "3.11"
disallow_untyped_defs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
markers = [
    "slow: marks tests as slow",
    "integration: marks tests as integration tests",
]
```

### .flake8

```ini
[flake8]
max-line-length = 127
max-complexity = 10
ignore = E203,E501,W503
exclude = .git,__pycache__,.venv,build,dist
```

## Environments and Secrets

### GitHub Environments

1. **staging**
   - Automatic deployment
   - Staging URL
   - Test data

2. **production**
   - Manual approval required
   - Production URL
   - Production secrets

### Required Secrets

```yaml
secrets:
  GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}  # Automatic
  SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}      # For Snyk scanning
  DOCKER_REGISTRY_TOKEN: ${{ secrets.DOCKER_REGISTRY_TOKEN }}
```

## Monitoring and Alerts

### Pipeline Metrics

- Build time
- Test success rate
- Security scan results
- Deployment frequency
- Lead time for changes

### Notifications

- ✅ Successful deployments
- ❌ Failed builds
- ⚠️ Security vulnerabilities
- 📊 Performance degradation

## Quality Gates

### Mandatory Checks

- ✅ All tests must pass
- ✅ Coverage > 80%
- ✅ Security scan without critical vulnerabilities
- ✅ Linting without errors
- ✅ Type checking without errors

### Performance Criteria

- ⚡ Average response time < 500ms
- 📈 95th percentile < 1000ms
- ❌ Error rate < 1%
- 🔄 Throughput > 100 RPS

## Local Development

### Pre-commit hooks

```bash
# Install pre-commit
pip install pre-commit
pre-commit install

# Run checks
pre-commit run --all-files
```

### Local Testing

```bash
# Full test suite
make test

# Unit tests only
make test-unit

# Integration tests only
make test-integration

# Performance tests
make test-performance

# Linting
make lint

# Security scan
make security-scan
```

## Troubleshooting

### Common Issues

1. **Tests fail in CI but pass locally**
   - Check environment variables
   - Ensure dependency versions match
   - Check services (postgres, redis)

2. **Docker build fails**
   - Check .dockerignore
   - Ensure Dockerfile correctness
   - Check context size

3. **Security scan finds vulnerabilities**
   - Update dependencies
   - Check safety-db
   - Exclude false positives

### Debugging

```bash
# Run GitHub Actions locally
act -j test

# Check Docker build
docker build -t bookstore-api:test .

# Local security scan
bandit -r bookstore/
safety check
```

## Metrics and KPIs

### DevOps Metrics

- **Deployment Frequency**: Daily
- **Lead Time**: < 2 hours
- **MTTR**: < 30 minutes
- **Change Failure Rate**: < 5%

### Quality Metrics

- **Test Coverage**: > 90%
- **Code Quality**: A grade
- **Security Score**: > 95%
- **Performance**: SLA compliance

## Next Steps

1. ✅ **CI/CD Pipeline** - implemented
2. 🔄 **Monitoring Integration** - in progress
3. ⏳ **Advanced Security** - planned
4. ⏳ **Multi-environment** - planned

The CI/CD system is ready for production use! 🚀