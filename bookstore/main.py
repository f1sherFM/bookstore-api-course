"""
Main FastAPI Application Entry Point

This is the heart of our BookStore API application. FastAPI is a modern, fast web framework
for building APIs with Python. This file sets up the entire application including:

- API routes and endpoints
- Database connections
- Authentication system
- Middleware for security, logging, and monitoring
- CORS (Cross-Origin Resource Sharing) configuration
- Health checks and metrics

For beginners: Think of this file as the "main control center" that coordinates
all the different parts of our bookstore system.
"""

# Import FastAPI core components
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware  # Allows web browsers to access our API
from fastapi.security import OAuth2PasswordRequestForm  # Handles login forms
from sqlalchemy.orm import Session  # Database session management
from datetime import timedelta  # For setting token expiration times
import uvicorn  # ASGI server to run our application

# Import our custom modules
from .database import get_db, init_db, get_database_info  # Database setup and connections
from .auth import authenticate_user, create_access_token, get_current_active_user  # User authentication
from .schemas import Token, User  # Data validation schemas
from .routers import books, authors, genres, users, reviews, reading_lists  # API route handlers
from .config import settings  # Application configuration
from .logging_config import get_logger, log_authentication_attempt  # Logging system
from .middleware import (  # Custom middleware for various features
    RequestLoggingMiddleware,  # Logs all incoming requests
    RateLimitMiddleware,      # Prevents API abuse by limiting requests
    SecurityHeadersMiddleware, # Adds security headers to responses
    MetricsMiddleware         # Collects performance metrics
)

# Initialize logging system
# Logging helps us track what's happening in our application and debug issues
logger = get_logger("bookstore.main")

# Create the main FastAPI application instance
# This is like creating a new web server that will handle HTTP requests
app = FastAPI(
    title=settings.app_name,           # Name shown in API documentation
    description=settings.description,   # Description shown in API docs
    version=settings.app_version,      # Current version of our API
    docs_url="/docs" if not settings.is_production else None,    # Swagger UI location (disabled in production for security)
    redoc_url="/redoc" if not settings.is_production else None,  # Alternative docs (disabled in production)
    debug=settings.debug               # Enable debug mode for development
)

# Add middleware layers (executed in reverse order - last added runs first)
# Middleware are like "filters" that process every request before it reaches our endpoints

# 1. Metrics collection (runs last, measures everything)
metrics_middleware = MetricsMiddleware(app)
app.add_middleware(MetricsMiddleware)

# 2. Security headers (adds security-related HTTP headers)
app.add_middleware(SecurityHeadersMiddleware)

# 3. Rate limiting (prevents API abuse by limiting requests per user)
app.add_middleware(RateLimitMiddleware)

# 4. Request logging (logs details about each request for debugging)
app.add_middleware(RequestLoggingMiddleware)

# Configure CORS (Cross-Origin Resource Sharing)
# This allows web browsers to make requests to our API from different domains
# Without CORS, a website at example.com couldn't call our API at api.bookstore.com
cors_config = settings.get_cors_config()
app.add_middleware(
    CORSMiddleware,
    **cors_config  # Spread operator - unpacks the configuration dictionary
)

# Register API routers - these handle different parts of our API
# Each router manages endpoints for a specific resource type
app.include_router(books.router, prefix="/api/v1/books", tags=["books"])
app.include_router(authors.router, prefix="/api/v1/authors", tags=["authors"])
app.include_router(genres.router, prefix="/api/v1/genres", tags=["genres"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(reviews.router, prefix="/api/v1/reviews", tags=["reviews"])
app.include_router(reading_lists.router, prefix="/api/v1/reading-lists", tags=["reading-lists"])

# Application Lifecycle Events
# These functions run when the application starts up and shuts down

@app.on_event("startup")
async def startup_event():
    """
    Application Startup Handler
    
    This function runs once when the application starts up.
    It's perfect for initialization tasks like:
    - Setting up database connections
    - Loading configuration
    - Initializing caches
    - Running database migrations
    
    For beginners: Think of this as the "setup" function that prepares
    everything before the API starts accepting requests.
    """
    logger.info(f"Starting {settings.app_name} v{settings.app_version}", extra={
        'extra_fields': {
            'environment': settings.environment,
            'debug': settings.debug,
            'event_type': 'application_startup'
        }
    })
    
    # Initialize the database (create tables, run migrations, add test data)
    init_db()
    logger.info("Database initialized successfully")
    
    # In development mode, show helpful information
    if settings.is_development:
        logger.info("API documentation available at: /docs")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Application Shutdown Handler
    
    This function runs when the application is shutting down.
    Use it for cleanup tasks like:
    - Closing database connections
    - Saving important data
    - Releasing resources
    
    For beginners: This is like the "cleanup" function that runs
    when the server is being turned off.
    """
    logger.info("Application shutdown", extra={
        'extra_fields': {
            'event_type': 'application_shutdown'
        }
    })


# API Endpoints
# These are the actual URLs that clients can call to interact with our API

@app.get("/")
async def root():
    """
    Root Endpoint - API Welcome Message
    
    This is the main entry point of our API. When someone visits the base URL
    (like https://api.bookstore.com/), they'll see basic information about our API.
    
    Returns:
        dict: Basic information about the API including version, environment, and available endpoints
        
    For beginners: This is like the "home page" of our API that tells visitors
    what they can do and where to find documentation.
    """
    logger.debug("Root endpoint accessed")
    
    return {
        "message": f"Welcome to {settings.app_name}!",
        "version": settings.app_version,
        "environment": settings.environment,
        "docs": "/docs" if not settings.is_production else "disabled",
        "health": "/health"
    }


@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """
    Health Check Endpoint - System Status Monitor
    
    This endpoint checks if our API and all its dependencies are working properly.
    It's essential for monitoring and deployment systems to know if the service is healthy.
    
    What it checks:
    - Database connectivity
    - Memory usage
    - Disk space
    - Configuration validity
    
    Args:
        db (Session): Database session injected by FastAPI's dependency system
        
    Returns:
        dict: Comprehensive health status including all system checks
        
    Raises:
        HTTPException: 503 Service Unavailable if any critical system is unhealthy
        
    For beginners: This is like a "system diagnostic" that tells us if everything
    is working correctly. Monitoring systems call this endpoint regularly to ensure
    the API is running smoothly.
    """
    from datetime import datetime
    import psutil  # System monitoring library
    
    # Create the base health status object
    health_status = {
        "status": "healthy",  # Overall status - will change to "unhealthy" if any check fails
        "timestamp": datetime.utcnow().isoformat() + "Z",  # When this check was performed
        "version": settings.app_version,
        "service": "bookstore-api",
        "environment": settings.environment,
        "checks": {}  # Individual check results will be stored here
    }
    
    # 1. Database Health Check
    # Try to connect to the database and run a simple query
    db_info = get_database_info()
    health_status["checks"]["database"] = db_info["status"]
    if db_info["status"] == "unhealthy":
        health_status["status"] = "unhealthy"
        health_status["checks"]["database_error"] = db_info.get("error", "Unknown error")
        logger.error("Database health check failed", extra={
            'extra_fields': {
                'error': db_info.get("error", "Unknown error"),
                'event_type': 'health_check_failed'
            }
        })
    
    # 2. Memory Usage Check
    # Monitor system memory to prevent out-of-memory crashes
    try:
        memory_percent = psutil.virtual_memory().percent
        if memory_percent < 90:
            health_status["checks"]["memory"] = "healthy"
        else:
            health_status["checks"]["memory"] = f"warning: {memory_percent}% used"
            if memory_percent > 95:  # Critical threshold
                health_status["status"] = "unhealthy"
                logger.warning(f"High memory usage: {memory_percent}%")
    except Exception as e:
        health_status["checks"]["memory"] = "unknown"
        logger.warning(f"Could not check memory usage: {e}")
    
    # 3. Disk Space Check
    # Ensure we have enough disk space for logs, database, etc.
    try:
        disk_usage = psutil.disk_usage('/').percent
        if disk_usage < 90:
            health_status["checks"]["disk_space"] = "healthy"
        else:
            health_status["checks"]["disk_space"] = f"warning: {disk_usage}% used"
            if disk_usage > 95:  # Critical threshold
                health_status["status"] = "unhealthy"
                logger.warning(f"High disk usage: {disk_usage}%")
    except Exception as e:
        health_status["checks"]["disk_space"] = "unknown"
        logger.warning(f"Could not check disk usage: {e}")
    
    # 4. Configuration Validation Check
    # Ensure critical configuration values are properly set
    config_issues = []
    if not settings.secret_key or len(settings.secret_key) < 16:
        config_issues.append("weak_secret_key")
    if not settings.jwt_secret_key or len(settings.jwt_secret_key) < 16:
        config_issues.append("weak_jwt_key")
    
    if not config_issues:
        health_status["checks"]["configuration"] = "healthy"
    else:
        health_status["checks"]["configuration"] = f"issues: {', '.join(config_issues)}"
        if settings.is_production:  # Configuration issues are critical in production
            health_status["status"] = "unhealthy"
            logger.error("Configuration issues detected", extra={
                'extra_fields': {
                    'issues': config_issues,
                    'event_type': 'config_validation_failed'
                }
            })
    
    # Log the overall health check result
    if health_status["status"] == "healthy":
        logger.debug("Health check passed")
    else:
        logger.error("Health check failed", extra={
            'extra_fields': {
                'health_status': health_status,
                'event_type': 'health_check_failed'
            }
        })
    
    # Return appropriate HTTP status code
    # 200 OK for healthy, 503 Service Unavailable for unhealthy
    if health_status["status"] == "unhealthy":
        raise HTTPException(status_code=503, detail=health_status)
    
    return health_status


@app.get("/metrics")
async def get_metrics():
    """
    Metrics Endpoint - Performance and Usage Statistics
    
    This endpoint provides detailed metrics about our API's performance and usage.
    It's used by monitoring systems like Prometheus to track:
    - Request counts and response times
    - Error rates
    - System resource usage
    
    Returns:
        dict: Performance metrics and statistics
        
    Raises:
        HTTPException: 404 Not Found if metrics are disabled in configuration
        
    For beginners: This endpoint is like a "dashboard" that shows how well
    our API is performing. Monitoring tools use this data to create graphs
    and alerts about system performance.
    """
    if not settings.metrics_enabled:
        raise HTTPException(status_code=404, detail="Metrics disabled")
    
    metrics = metrics_middleware.get_metrics()
    logger.debug("Metrics endpoint accessed", extra={
        'extra_fields': {
            'total_requests': metrics.get('requests_total', 0),
            'event_type': 'metrics_access'
        }
    })
    
    return metrics


@app.get("/info")
async def app_info():
    """
    Application Information Endpoint
    
    Provides detailed information about the application configuration and features.
    This is useful for:
    - Debugging configuration issues
    - Understanding what features are enabled
    - API version information
    
    Returns:
        dict: Application configuration and feature information
        
    For beginners: This endpoint tells you everything about how the API
    is configured - what features are turned on, what limits are set, etc.
    It's like looking at the "settings" of our application.
    """
    logger.debug("Info endpoint accessed")
    
    return {
        "app_name": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "debug": settings.debug,
        "features": {
            "cache_enabled": settings.cache_enabled,
            "metrics_enabled": settings.metrics_enabled,
            "docs_enabled": not settings.is_production
        },
        "limits": {
            "rate_limit_per_minute": settings.rate_limit_per_minute,
            "max_page_size": settings.max_page_size,
            "max_file_size": settings.max_file_size
        }
    }


@app.post("/auth/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    User Authentication Endpoint - Login
    
    This endpoint handles user login and returns a JWT (JSON Web Token) for authentication.
    The JWT token is used to authenticate subsequent API requests.
    
    How it works:
    1. User provides username and password
    2. We verify the credentials against the database
    3. If valid, we create a JWT token with an expiration time
    4. The client uses this token in the Authorization header for future requests
    
    Args:
        form_data (OAuth2PasswordRequestForm): Login form with username and password
        db (Session): Database session for user lookup
        
    Returns:
        Token: JWT access token and token type
        
    Raises:
        HTTPException: 401 Unauthorized if credentials are invalid
        
    For beginners: This is like the "login page" of our API. Users send their
    username and password here, and if they're correct, they get a "ticket" (JWT token)
    that proves they're logged in for future requests.
    """
    username = form_data.username
    
    # Log the authentication attempt for security monitoring
    logger.info(f"Authentication attempt for user: {username}", extra={
        'extra_fields': {
            'username': username,
            'event_type': 'auth_attempt'
        }
    })
    
    # Verify the user's credentials
    user = authenticate_user(db, username, form_data.password)
    
    if not user:
        # Log failed authentication for security monitoring
        log_authentication_attempt(username, success=False)
        logger.warning(f"Failed authentication for user: {username}")
        
        # Return a generic error message to prevent username enumeration attacks
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Log successful authentication
    log_authentication_attempt(username, success=True)
    logger.info(f"Successful authentication for user: {username}", extra={
        'extra_fields': {
            'user_id': str(user.id),
            'username': username,
            'event_type': 'auth_success'
        }
    })
    
    # Create JWT token with expiration time
    access_token_expires = timedelta(minutes=settings.jwt_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/auth/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """
    Get Current User Information
    
    This endpoint returns information about the currently authenticated user.
    It requires a valid JWT token in the Authorization header.
    
    Args:
        current_user (User): Current authenticated user (injected by dependency)
        
    Returns:
        User: Current user's profile information
        
    For beginners: This is like a "profile page" that shows information about
    the user who is currently logged in. The user must include their JWT token
    to prove who they are.
    """
    logger.debug(f"User profile accessed by: {current_user.username}", extra={
        'extra_fields': {
            'user_id': str(current_user.id),
            'username': current_user.username,
            'event_type': 'profile_access'
        }
    })
    
    return current_user


# Application Entry Point
# This section runs when the file is executed directly (not imported as a module)
if __name__ == "__main__":
    """
    Development Server Entry Point
    
    This code runs when you execute this file directly with Python.
    It starts a development server using Uvicorn (ASGI server).
    
    Configuration:
    - host="0.0.0.0": Accept connections from any IP address
    - port=8000: Listen on port 8000
    - reload=True: Automatically restart when code changes (development only)
    - workers=1: Use single worker in development for easier debugging
    
    For beginners: This is like the "start button" for our API server.
    When you run this file, it starts the web server that listens for
    HTTP requests and responds with our API.
    """
    uvicorn.run(
        "bookstore.main:app",  # Module path to our FastAPI app
        host="0.0.0.0",        # Listen on all network interfaces
        port=8000,             # Port number to listen on
        reload=settings.is_development,  # Auto-reload on code changes (development only)
        log_level=settings.log_level.lower(),  # Logging verbosity
        workers=1 if settings.is_development else settings.workers  # Number of worker processes
    )