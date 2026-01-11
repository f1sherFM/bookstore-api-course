#!/bin/bash

# BookStore API - Development Environment Setup Script
# This script sets up a complete development environment

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running on Windows (Git Bash/WSL)
is_windows() {
    [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]] || [[ -n "$WSL_DISTRO_NAME" ]]
}

# Main setup function
main() {
    log_info "🚀 Setting up BookStore API development environment..."
    echo
    
    # Check prerequisites
    log_info "Checking prerequisites..."
    
    # Check Python
    if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null; then
        log_error "Python is not installed. Please install Python 3.11+ first."
        exit 1
    fi
    
    # Check pip
    if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
        log_error "pip is not installed. Please install pip first."
        exit 1
    fi
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        log_warning "Docker is not installed. Some features will not be available."
        log_info "Install Docker from: https://docs.docker.com/get-docker/"
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        log_warning "Docker Compose is not installed. Some features will not be available."
        log_info "Install Docker Compose from: https://docs.docker.com/compose/install/"
    fi
    
    log_success "Prerequisites check completed"
    echo
    
    # Create virtual environment
    log_info "Creating Python virtual environment..."
    
    if [ -d "venv" ]; then
        log_warning "Virtual environment already exists. Skipping creation."
    else
        python -m venv venv || python3 -m venv venv
        log_success "Virtual environment created"
    fi
    
    # Activate virtual environment
    log_info "Activating virtual environment..."
    
    if is_windows; then
        source venv/Scripts/activate
    else
        source venv/bin/activate
    fi
    
    log_success "Virtual environment activated"
    echo
    
    # Upgrade pip
    log_info "Upgrading pip..."
    pip install --upgrade pip
    log_success "pip upgraded"
    
    # Install dependencies
    log_info "Installing Python dependencies..."
    
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
        log_success "Core dependencies installed"
    fi
    
    if [ -f "fastapi_requirements.txt" ]; then
        pip install -r fastapi_requirements.txt
        log_success "FastAPI dependencies installed"
    fi
    
    if [ -f "testing_requirements.txt" ]; then
        pip install -r testing_requirements.txt
        log_success "Testing dependencies installed"
    fi
    
    echo
    
    # Create environment file
    log_info "Setting up environment configuration..."
    
    if [ ! -f ".env" ]; then
        if [ -f ".env.example" ]; then
            cp .env.example .env
            log_success "Environment file created from example"
        else
            # Create basic .env file
            cat > .env << EOF
# BookStore API - Development Environment
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=DEBUG
LOG_FORMAT=text

# Database (SQLite for development)
DATABASE_URL=sqlite:///./bookstore.db
DATABASE_ECHO=true

# Redis (optional for development)
REDIS_URL=redis://localhost:6379
CACHE_ENABLED=false

# Security (development keys - change in production!)
SECRET_KEY=dev-secret-key-change-in-production-32-chars
JWT_SECRET_KEY=dev-jwt-secret-change-in-production-32-chars
JWT_EXPIRE_MINUTES=60

# CORS (allow all for development)
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080,http://localhost:3001
ALLOWED_METHODS=GET,POST,PUT,DELETE,OPTIONS
ALLOWED_HEADERS=*

# Rate Limiting (relaxed for development)
RATE_LIMIT_PER_MINUTE=1000
AUTH_RATE_LIMIT_PER_MINUTE=100

# Performance
WORKERS=1
MAX_CONNECTIONS=100
CONNECTION_TIMEOUT=30

# Monitoring
METRICS_ENABLED=true
HEALTH_CHECK_INTERVAL=30
EOF
            log_success "Basic environment file created"
        fi
    else
        log_warning "Environment file already exists. Skipping creation."
    fi
    
    echo
    
    # Initialize database
    log_info "Initializing database..."
    
    if command -v python &> /dev/null; then
        python -c "
from bookstore.database import engine, Base
from bookstore.models import *
Base.metadata.create_all(bind=engine)
print('Database tables created successfully')
" 2>/dev/null || log_warning "Could not initialize database. Run manually after starting the app."
    fi
    
    # Create test data
    log_info "Creating test data..."
    
    if [ -f "create_test_data.py" ]; then
        python create_test_data.py 2>/dev/null || log_warning "Could not create test data. Run manually if needed."
        log_success "Test data created"
    fi
    
    echo
    
    # Run tests to verify setup
    log_info "Running tests to verify setup..."
    
    if command -v pytest &> /dev/null; then
        pytest tests/test_unit_basic.py -v --tb=short -q || log_warning "Some tests failed. Check the output above."
        log_success "Basic tests completed"
    else
        log_warning "pytest not available. Install testing dependencies to run tests."
    fi
    
    echo
    
    # Setup Docker environment (if Docker is available)
    if command -v docker &> /dev/null && command -v docker-compose &> /dev/null; then
        log_info "Setting up Docker development environment..."
        
        # Build Docker image
        docker build -t bookstore-api:dev . || log_warning "Docker build failed"
        
        # Start development services
        log_info "Starting development services with Docker..."
        docker-compose up -d db redis || log_warning "Could not start all Docker services"
        
        log_success "Docker environment setup completed"
    fi
    
    echo
    
    # Final success message
    log_success "🎉 Development environment setup completed!"
    echo
    echo "Next steps:"
    echo "==========="
    echo "1. Activate virtual environment:"
    if is_windows; then
        echo "   source venv/Scripts/activate"
    else
        echo "   source venv/bin/activate"
    fi
    echo
    echo "2. Start the development server:"
    echo "   python run_bookstore.py"
    echo "   # or"
    echo "   make dev"
    echo
    echo "3. Open your browser:"
    echo "   API: http://localhost:8000"
    echo "   Docs: http://localhost:8000/docs"
    echo "   Health: http://localhost:8000/health"
    echo
    echo "4. Run tests:"
    echo "   pytest tests/ -v"
    echo "   # or"
    echo "   make test"
    echo
    echo "5. View available commands:"
    echo "   make help"
    echo
    echo "Happy coding! 🚀"
}

# Handle script arguments
case "${1:-setup}" in
    "setup")
        main
        ;;
    "clean")
        log_info "Cleaning development environment..."
        
        # Remove virtual environment
        if [ -d "venv" ]; then
            rm -rf venv
            log_success "Virtual environment removed"
        fi
        
        # Remove database
        if [ -f "bookstore.db" ]; then
            rm bookstore.db
            log_success "Database removed"
        fi
        
        # Remove cache directories
        find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
        find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
        find . -type d -name ".hypothesis" -exec rm -rf {} + 2>/dev/null || true
        
        # Stop Docker services
        if command -v docker-compose &> /dev/null; then
            docker-compose down -v 2>/dev/null || true
        fi
        
        log_success "Development environment cleaned"
        ;;
    "test")
        log_info "Running development environment tests..."
        
        # Activate virtual environment
        if [ -d "venv" ]; then
            if is_windows; then
                source venv/Scripts/activate
            else
                source venv/bin/activate
            fi
        fi
        
        # Run tests
        if command -v pytest &> /dev/null; then
            pytest tests/ -v
        else
            log_error "pytest not available. Run setup first."
            exit 1
        fi
        ;;
    "docker")
        log_info "Setting up Docker-only development environment..."
        
        if ! command -v docker &> /dev/null || ! command -v docker-compose &> /dev/null; then
            log_error "Docker and Docker Compose are required for this option"
            exit 1
        fi
        
        # Create environment file if it doesn't exist
        if [ ! -f ".env" ]; then
            cp .env.example .env 2>/dev/null || echo "DATABASE_URL=sqlite:///./bookstore.db" > .env
        fi
        
        # Start all services
        docker-compose up -d
        
        log_success "Docker development environment started"
        echo "API available at: http://localhost:8000"
        echo "Docs available at: http://localhost:8000/docs"
        ;;
    *)
        echo "Usage: $0 {setup|clean|test|docker}"
        echo
        echo "Commands:"
        echo "  setup  - Set up complete development environment (default)"
        echo "  clean  - Clean up development environment"
        echo "  test   - Run tests to verify setup"
        echo "  docker - Set up Docker-only environment"
        exit 1
        ;;
esac