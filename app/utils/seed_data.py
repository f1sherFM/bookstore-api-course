"""Seed data for BookStore API roadmap based on actual project structure."""

from app import db
from app.models.node import Node


def create_bookstore_roadmap():
    """Create BookStore API roadmap seed data based on actual project learning paths."""
    
    # GitHub repository base URL
    GITHUB_BASE = "https://github.com/f1sherFM/bookstore-api-course"
    
    # Root level - BookStore API Learning Roadmap
    bookstore_root = Node(
        title="📚 BookStore API Learning Roadmap",
        description="Production-ready FastAPI system - from beginner to DevOps expert",
        node_type="root",
        github_url=f"{GITHUB_BASE}"
    )
    db.session.add(bookstore_root)
    db.session.flush()  # Get ID for parent reference
    
    # 1. Quick Explorer (5 minutes)
    quick_explorer = Node(
        title="🚀 Quick Explorer (5 min)",
        description="Just want to see it work? Get the API running and make your first request",
        node_type="basic",
        parent_id=bookstore_root.id,
        github_url=f"{GITHUB_BASE}#-quick-explorer-5-minutes"
    )
    db.session.add(quick_explorer)
    db.session.flush()
    
    # Quick Explorer steps
    quick_steps = [
        ("Setup Environment", "Clone repo and setup development environment", "basic", f"{GITHUB_BASE}/blob/main/QUICK_START.md"),
        ("Start Development Server", "Run the API locally", "basic", f"{GITHUB_BASE}/blob/main/run_bookstore.py"),
        ("Explore API Documentation", "Interactive Swagger UI", "basic", f"{GITHUB_BASE}#-api-documentation"),
        ("Test Health Endpoint", "Check if API is running", "basic", f"{GITHUB_BASE}/blob/main/bookstore/routers/health.py"),
        ("Create First User", "Register via /auth/register", "basic", f"{GITHUB_BASE}/blob/main/bookstore/auth.py"),
        ("Get Books List", "Try /api/v1/books/ endpoint", "basic", f"{GITHUB_BASE}/blob/main/bookstore/routers/books.py")
    ]
    
    for title, desc, node_type, github_url in quick_steps:
        node = Node(title=title, description=desc, node_type=node_type, parent_id=quick_explorer.id, github_url=github_url)
        db.session.add(node)
    
    # 2. API User (30 minutes)
    api_user = Node(
        title="📱 API User (30 min)",
        description="Want to integrate with the API? Learn authentication, core operations, and advanced features",
        node_type="basic",
        parent_id=bookstore_root.id,
        github_url=f"{GITHUB_BASE}#-api-user-30-minutes"
    )
    db.session.add(api_user)
    db.session.flush()
    
    # Authentication Flow
    auth_flow = Node(
        title="Authentication Flow",
        description="Learn JWT authentication and user management",
        node_type="basic",
        parent_id=api_user.id,
        github_url=f"{GITHUB_BASE}/blob/main/bookstore/auth.py"
    )
    db.session.add(auth_flow)
    db.session.flush()
    
    auth_steps = [
        ("Register New User", "POST /auth/register", "basic", f"{GITHUB_BASE}/blob/main/bookstore/routers/users.py"),
        ("Login & Get JWT Token", "POST /auth/login", "basic", f"{GITHUB_BASE}/blob/main/bookstore/auth.py"),
        ("Use Token in Headers", "Authorization: Bearer <token>", "basic", f"{GITHUB_BASE}/blob/main/QUICK_START.md#authentication"),
        ("Refresh Token", "POST /auth/refresh", "basic", f"{GITHUB_BASE}/blob/main/bookstore/auth.py")
    ]
    
    for title, desc, node_type, github_url in auth_steps:
        node = Node(title=title, description=desc, node_type=node_type, parent_id=auth_flow.id, github_url=github_url)
        db.session.add(node)
    
    # Core Operations
    core_ops = Node(
        title="Core Operations",
        description="Essential API operations for books and users",
        node_type="basic",
        parent_id=api_user.id,
        github_url=f"{GITHUB_BASE}/blob/main/bookstore/routers"
    )
    db.session.add(core_ops)
    db.session.flush()
    
    core_steps = [
        ("List Books with Pagination", "GET /api/v1/books/?page=1&size=10", "basic", f"{GITHUB_BASE}/blob/main/bookstore/routers/books.py"),
        ("Search Books", "GET /api/v1/books/?q=python", "basic", f"{GITHUB_BASE}/blob/main/bookstore/routers/books.py"),
        ("Get Book Details", "GET /api/v1/books/{{id}}", "basic", f"{GITHUB_BASE}/blob/main/bookstore/routers/books.py"),
        ("Add to Reading List", "POST /api/v1/reading-lists/books/{{id}}", "basic", f"{GITHUB_BASE}/blob/main/bookstore/routers/reading_lists.py"),
        ("Write Book Review", "POST /api/v1/books/{{id}}/reviews", "basic", f"{GITHUB_BASE}/blob/main/bookstore/routers/reviews.py")
    ]
    
    for title, desc, node_type, github_url in core_steps:
        node = Node(title=title, description=desc, node_type=node_type, parent_id=core_ops.id, github_url=github_url)
        db.session.add(node)
    
    # 3. Developer (2 hours)
    developer = Node(
        title="👨‍💻 Developer (2 hours)",
        description="Understand the codebase and make your first contribution",
        node_type="intermediate",
        parent_id=bookstore_root.id,
        github_url=f"{GITHUB_BASE}#-developer-2-hours"
    )
    db.session.add(developer)
    db.session.flush()
    
    # Code Structure
    code_structure = Node(
        title="Code Structure",
        description="Explore the FastAPI application architecture",
        node_type="intermediate",
        parent_id=developer.id,
        github_url=f"{GITHUB_BASE}/blob/main/PROJECT_STRUCTURE.md"
    )
    db.session.add(code_structure)
    db.session.flush()
    
    structure_items = [
        ("Main Application", "FastAPI app setup and configuration", "intermediate", f"{GITHUB_BASE}/blob/main/bookstore/main.py"),
        ("Database Models", "SQLAlchemy models for books, users, reviews", "intermediate", f"{GITHUB_BASE}/blob/main/bookstore/models.py"),
        ("Pydantic Schemas", "Data validation and serialization", "intermediate", f"{GITHUB_BASE}/blob/main/bookstore/schemas.py"),
        ("API Routers", "Organized endpoint handlers", "intermediate", f"{GITHUB_BASE}/tree/main/bookstore/routers"),
        ("Authentication System", "JWT and security implementation", "intermediate", f"{GITHUB_BASE}/blob/main/bookstore/auth.py"),
        ("Database Configuration", "Connection and session management", "intermediate", f"{GITHUB_BASE}/blob/main/bookstore/database.py")
    ]
    
    for title, desc, node_type, github_url in structure_items:
        node = Node(title=title, description=desc, node_type=node_type, parent_id=code_structure.id, github_url=github_url)
        db.session.add(node)
    
    # Development Workflow
    dev_workflow = Node(
        title="Development Workflow",
        description="Learn the development process and tools",
        node_type="intermediate",
        parent_id=developer.id,
        github_url=f"{GITHUB_BASE}/blob/main/Makefile"
    )
    db.session.add(dev_workflow)
    db.session.flush()
    
    workflow_items = [
        ("Setup Development Environment", "make install", "intermediate", f"{GITHUB_BASE}/blob/main/QUICK_START.md#development"),
        ("Run Tests", "make test", "intermediate", f"{GITHUB_BASE}/tree/main/tests"),
        ("Code Formatting", "make format", "intermediate", f"{GITHUB_BASE}/blob/main/Makefile"),
        ("Add New Endpoint", "Create a genre endpoint example", "intermediate", f"{GITHUB_BASE}/blob/main/development/examples"),
        ("Database Migrations", "Alembic migration system", "intermediate", f"{GITHUB_BASE}/tree/main/alembic")
    ]
    
    for title, desc, node_type, github_url in workflow_items:
        node = Node(title=title, description=desc, node_type=node_type, parent_id=dev_workflow.id, github_url=github_url)
        db.session.add(node)
    
    # Testing Deep Dive
    testing_dive = Node(
        title="Testing Deep Dive",
        description="Comprehensive testing strategies and implementation",
        node_type="intermediate",
        parent_id=developer.id,
        github_url=f"{GITHUB_BASE}/tree/main/tests"
    )
    db.session.add(testing_dive)
    db.session.flush()
    
    testing_items = [
        ("Unit Tests", "Test individual components", "intermediate", f"{GITHUB_BASE}/blob/main/tests/test_unit_basic.py"),
        ("Integration Tests", "Test API endpoints", "intermediate", f"{GITHUB_BASE}/blob/main/tests/test_api_integration.py"),
        ("Property-Based Tests", "Hypothesis testing framework", "advanced", f"{GITHUB_BASE}/blob/main/tests/test_property_based.py"),
        ("Performance Tests", "Load testing with Locust", "advanced", f"{GITHUB_BASE}/blob/main/tests/test_performance.py"),
        ("Test Factories", "Generate test data", "intermediate", f"{GITHUB_BASE}/blob/main/tests/factories.py"),
        ("Test Configuration", "Pytest setup and fixtures", "intermediate", f"{GITHUB_BASE}/blob/main/tests/conftest.py")
    ]
    
    for title, desc, node_type, github_url in testing_items:
        node = Node(title=title, description=desc, node_type=node_type, parent_id=testing_dive.id, github_url=github_url)
        db.session.add(node)
    
    # 4. Production User (1 hour)
    production_user = Node(
        title="🏭 Production User (1 hour)",
        description="Deploy and monitor the API in production",
        node_type="intermediate",
        parent_id=bookstore_root.id,
        github_url=f"{GITHUB_BASE}#-production-user-1-hour"
    )
    db.session.add(production_user)
    db.session.flush()
    
    # Docker Deployment
    docker_deploy = Node(
        title="Docker Deployment",
        description="Containerized deployment with Docker Compose",
        node_type="intermediate",
        parent_id=production_user.id,
        github_url=f"{GITHUB_BASE}/tree/main/deployment/docker"
    )
    db.session.add(docker_deploy)
    db.session.flush()
    
    docker_items = [
        ("Local Production Stack", "make docker-prod", "intermediate", f"{GITHUB_BASE}/blob/main/deployment/docker/docker-compose.prod.yml"),
        ("Environment Configuration", "Production environment variables", "intermediate", f"{GITHUB_BASE}/blob/main/.env.production"),
        ("SSL Setup", "HTTPS and domain configuration", "intermediate", f"{GITHUB_BASE}/blob/main/deployment/docker/nginx.conf"),
        ("Multi-stage Dockerfile", "Optimized container builds", "intermediate", f"{GITHUB_BASE}/blob/main/deployment/docker/Dockerfile")
    ]
    
    for title, desc, node_type, github_url in docker_items:
        node = Node(title=title, description=desc, node_type=node_type, parent_id=docker_deploy.id, github_url=github_url)
        db.session.add(node)
    
    # Monitoring Setup
    monitoring = Node(
        title="Monitoring Setup",
        description="Observability and performance monitoring",
        node_type="intermediate",
        parent_id=production_user.id,
        github_url=f"{GITHUB_BASE}/tree/main/deployment/monitoring"
    )
    db.session.add(monitoring)
    db.session.flush()
    
    monitoring_items = [
        ("Grafana Dashboards", "Performance visualization", "intermediate", f"{GITHUB_BASE}/tree/main/deployment/monitoring/grafana"),
        ("Prometheus Metrics", "Application metrics collection", "intermediate", f"{GITHUB_BASE}/tree/main/deployment/monitoring/prometheus"),
        ("Log Aggregation", "Structured logging with Loki", "intermediate", f"{GITHUB_BASE}/blob/main/bookstore/logging_config.py"),
        ("Health Check Endpoints", "Service status monitoring", "intermediate", f"{GITHUB_BASE}/blob/main/development/scripts/production-health-check.sh")
    ]
    
    for title, desc, node_type, github_url in monitoring_items:
        node = Node(title=title, description=desc, node_type=node_type, parent_id=monitoring.id, github_url=github_url)
        db.session.add(node)
    
    # 5. DevOps Engineer (3 hours)
    devops_engineer = Node(
        title="☸️ DevOps Engineer (3 hours)",
        description="Master the complete DevOps pipeline and infrastructure",
        node_type="advanced",
        parent_id=bookstore_root.id,
        github_url=f"{GITHUB_BASE}#️-devops-engineer-3-hours"
    )
    db.session.add(devops_engineer)
    db.session.flush()
    
    # Containerization Mastery
    containerization = Node(
        title="Containerization Mastery",
        description="Advanced Docker and container orchestration",
        node_type="advanced",
        parent_id=devops_engineer.id,
        github_url=f"{GITHUB_BASE}/tree/main/deployment/docker"
    )
    db.session.add(containerization)
    db.session.flush()
    
    container_items = [
        ("Multi-stage Dockerfile", "Optimized container builds", "advanced", f"{GITHUB_BASE}/blob/main/deployment/docker/Dockerfile"),
        ("Docker Compose Environments", "Development and production stacks", "advanced", f"{GITHUB_BASE}/tree/main/deployment/docker"),
        ("Container Security", "Security scanning and best practices", "advanced", f"{GITHUB_BASE}/blob/main/.github/workflows/ci.yml"),
        ("Registry Management", "GitHub Container Registry", "advanced", f"{GITHUB_BASE}/blob/main/.github/workflows/ci.yml")
    ]
    
    for title, desc, node_type, github_url in container_items:
        node = Node(title=title, description=desc, node_type=node_type, parent_id=containerization.id, github_url=github_url)
        db.session.add(node)
    
    # Kubernetes Deployment
    k8s_deploy = Node(
        title="Kubernetes Deployment",
        description="Cloud-native deployment with Kubernetes",
        node_type="advanced",
        parent_id=devops_engineer.id,
        github_url=f"{GITHUB_BASE}/tree/main/deployment/k8s"
    )
    db.session.add(k8s_deploy)
    db.session.flush()
    
    k8s_items = [
        ("Kubernetes Manifests", "Deployment, services, ingress", "advanced", f"{GITHUB_BASE}/tree/main/deployment/k8s"),
        ("Auto-scaling Configuration", "Horizontal Pod Autoscaler", "advanced", f"{GITHUB_BASE}/blob/main/deployment/k8s/hpa.yaml"),
        ("Ingress & Service Mesh", "Traffic management", "advanced", f"{GITHUB_BASE}/blob/main/deployment/k8s/ingress.yaml"),
        ("Persistent Storage", "Database and cache persistence", "advanced", f"{GITHUB_BASE}/blob/main/deployment/k8s/postgresql.yaml")
    ]
    
    for title, desc, node_type, github_url in k8s_items:
        node = Node(title=title, description=desc, node_type=node_type, parent_id=k8s_deploy.id, github_url=github_url)
        db.session.add(node)
    
    # CI/CD Pipeline
    cicd_pipeline = Node(
        title="CI/CD Pipeline",
        description="Automated testing and deployment",
        node_type="advanced",
        parent_id=devops_engineer.id,
        github_url=f"{GITHUB_BASE}/tree/main/.github/workflows"
    )
    db.session.add(cicd_pipeline)
    db.session.flush()
    
    cicd_items = [
        ("GitHub Actions Workflows", "Automated CI/CD pipeline", "advanced", f"{GITHUB_BASE}/blob/main/.github/workflows/ci.yml"),
        ("Automated Testing", "Unit, integration, performance tests", "advanced", f"{GITHUB_BASE}/blob/main/.github/workflows/ci.yml"),
        ("Security Scanning", "Vulnerability and dependency scanning", "advanced", f"{GITHUB_BASE}/blob/main/.github/workflows/dependencies.yml"),
        ("Multi-environment Deployment", "Staging and production", "advanced", f"{GITHUB_BASE}/blob/main/.github/workflows/performance.yml")
    ]
    
    for title, desc, node_type, github_url in cicd_items:
        node = Node(title=title, description=desc, node_type=node_type, parent_id=cicd_pipeline.id, github_url=github_url)
        db.session.add(node)
    
    # 6. Learning Path (Ongoing)
    learning_path = Node(
        title="🎓 Learning Path (Ongoing)",
        description="Use this project as a learning resource for modern Python and DevOps",
        node_type="advanced",
        parent_id=bookstore_root.id,
        github_url=f"{GITHUB_BASE}#-learning-path-ongoing"
    )
    db.session.add(learning_path)
    db.session.flush()
    
    # Python & FastAPI Fundamentals
    python_fundamentals = Node(
        title="Python & FastAPI Fundamentals",
        description="Modern Python development practices",
        node_type="intermediate",
        parent_id=learning_path.id,
        github_url=f"{GITHUB_BASE}/tree/main/development/examples"
    )
    db.session.add(python_fundamentals)
    db.session.flush()
    
    python_items = [
        ("FastAPI Cheatsheet", "Complete FastAPI reference", "intermediate", f"{GITHUB_BASE}/blob/main/development/examples/fastapi_cheatsheet.md"),
        ("OOP Practice", "Object-oriented programming examples", "intermediate", f"{GITHUB_BASE}/blob/main/development/examples/oop_practice.py"),
        ("Type Hints Advanced", "Advanced typing patterns", "intermediate", f"{GITHUB_BASE}/blob/main/development/examples/type_hints_advanced.py"),
        ("Decorators Guide", "Advanced decorator patterns", "advanced", f"{GITHUB_BASE}/blob/main/development/examples/decorators_advanced.py"),
        ("Async Programming", "Async/await patterns", "advanced", f"{GITHUB_BASE}/blob/main/bookstore/main.py")
    ]
    
    for title, desc, node_type, github_url in python_items:
        node = Node(title=title, description=desc, node_type=node_type, parent_id=python_fundamentals.id, github_url=github_url)
        db.session.add(node)
    
    # Testing Methodologies
    testing_methods = Node(
        title="Testing Methodologies",
        description="Comprehensive testing strategies",
        node_type="intermediate",
        parent_id=learning_path.id,
        github_url=f"{GITHUB_BASE}/tree/main/tests"
    )
    db.session.add(testing_methods)
    db.session.flush()
    
    testing_method_items = [
        ("Testing Cheatsheet", "Complete testing reference", "intermediate", f"{GITHUB_BASE}/blob/main/development/examples/testing_cheatsheet.md"),
        ("Property-Based Testing", "Hypothesis framework examples", "advanced", f"{GITHUB_BASE}/blob/main/tests/test_property_based.py"),
        ("Performance Testing", "Load testing with Locust", "advanced", f"{GITHUB_BASE}/blob/main/tests/test_performance.py"),
        ("Integration Testing", "API endpoint testing", "intermediate", f"{GITHUB_BASE}/blob/main/tests/test_api_integration.py"),
        ("Test Factories", "Data generation patterns", "intermediate", f"{GITHUB_BASE}/blob/main/tests/factories.py")
    ]
    
    for title, desc, node_type, github_url in testing_method_items:
        node = Node(title=title, description=desc, node_type=node_type, parent_id=testing_methods.id, github_url=github_url)
        db.session.add(node)
    
    # DevOps & Infrastructure
    devops_infra = Node(
        title="DevOps & Infrastructure",
        description="Production-ready infrastructure patterns",
        node_type="advanced",
        parent_id=learning_path.id,
        github_url=f"{GITHUB_BASE}/tree/main/deployment"
    )
    db.session.add(devops_infra)
    db.session.flush()
    
    devops_items = [
        ("Docker Best Practices", "Container optimization guide", "advanced", f"{GITHUB_BASE}/blob/main/documentation/guides/DOCKER_DEVOPS_GUIDE.md"),
        ("Kubernetes Deployment", "Cloud-native deployment", "advanced", f"{GITHUB_BASE}/tree/main/deployment/k8s"),
        ("CI/CD Pipelines", "Automated deployment workflows", "advanced", f"{GITHUB_BASE}/tree/main/.github/workflows"),
        ("Monitoring & Observability", "Production monitoring setup", "advanced", f"{GITHUB_BASE}/tree/main/deployment/monitoring"),
        ("Security Practices", "Application security patterns", "advanced", f"{GITHUB_BASE}/blob/main/bookstore/auth.py")
    ]
    
    for title, desc, node_type, github_url in devops_items:
        node = Node(title=title, description=desc, node_type=node_type, parent_id=devops_infra.id, github_url=github_url)
        db.session.add(node)
    
    # Production Readiness
    production_ready = Node(
        title="Production Readiness",
        description="Enterprise-grade deployment practices",
        node_type="advanced",
        parent_id=learning_path.id,
        github_url=f"{GITHUB_BASE}/blob/main/documentation/guides/PRODUCTION_DEPLOYMENT.md"
    )
    db.session.add(production_ready)
    db.session.flush()
    
    production_items = [
        ("Security Practices", "Application security implementation", "advanced", f"{GITHUB_BASE}/blob/main/documentation/guides/PRODUCTION_DEPLOYMENT.md"),
        ("Performance Optimization", "Scaling and optimization", "advanced", f"{GITHUB_BASE}/blob/main/documentation/guides/TESTING_GUIDE.md"),
        ("Backup & Recovery", "Data protection strategies", "advanced", f"{GITHUB_BASE}/blob/main/development/scripts/backup-script.sh"),
        ("Health Monitoring", "Production health checks", "advanced", f"{GITHUB_BASE}/blob/main/development/scripts/production-health-check.sh"),
        ("Incident Response", "Monitoring and alerting", "advanced", f"{GITHUB_BASE}/tree/main/deployment/monitoring")
    ]
    
    for title, desc, node_type, github_url in production_items:
        node = Node(title=title, description=desc, node_type=node_type, parent_id=production_ready.id, github_url=github_url)
        db.session.add(node)
    
    # Commit all changes
    db.session.commit()
    print("BookStore API roadmap seed data created successfully!")