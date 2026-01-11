"""
Main FastAPI application with logging and middleware
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
import uvicorn

from .database import get_db, init_db, get_database_info
from .auth import authenticate_user, create_access_token, get_current_active_user
from .schemas import Token, User
from .routers import books, authors, genres, users, reviews, reading_lists
from .config import settings
from .logging_config import get_logger, log_authentication_attempt
from .middleware import (
    RequestLoggingMiddleware, 
    RateLimitMiddleware, 
    SecurityHeadersMiddleware,
    MetricsMiddleware
)

# Initialize logging
logger = get_logger("bookstore.main")

# Create FastAPI application with settings
app = FastAPI(
    title=settings.app_name,
    description=settings.description,
    version=settings.app_version,
    docs_url="/docs" if not settings.is_production else None,
    redoc_url="/redoc" if not settings.is_production else None,
    debug=settings.debug
)

# Add middleware in correct order (last added executes first)
metrics_middleware = MetricsMiddleware(app)
app.add_middleware(MetricsMiddleware)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(RequestLoggingMiddleware)

# Configure CORS using configuration
cors_config = settings.get_cors_config()
app.add_middleware(
    CORSMiddleware,
    **cors_config
)

# Connect routers
app.include_router(books.router, prefix="/api/v1/books", tags=["books"])
app.include_router(authors.router, prefix="/api/v1/authors", tags=["authors"])
app.include_router(genres.router, prefix="/api/v1/genres", tags=["genres"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(reviews.router, prefix="/api/v1/reviews", tags=["reviews"])
app.include_router(reading_lists.router, prefix="/api/v1/reading-lists", tags=["reading-lists"])


@app.on_event("startup")
async def startup_event():
    """Initialization on startup"""
    logger.info(f"Starting {settings.app_name} v{settings.app_version}", extra={
        'extra_fields': {
            'environment': settings.environment,
            'debug': settings.debug,
            'event_type': 'application_startup'
        }
    })
    
    init_db()
    logger.info("Database initialized successfully")
    
    if settings.is_development:
        logger.info("API documentation available at: /docs")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Application shutdown", extra={
        'extra_fields': {
            'event_type': 'application_shutdown'
        }
    })


@app.get("/")
async def root():
    """Root endpoint with application information"""
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
    """Comprehensive service health check"""
    from datetime import datetime
    import psutil
    
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "version": settings.app_version,
        "service": "bookstore-api",
        "environment": settings.environment,
        "checks": {}
    }
    
    # Database check
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
    
    # Memory usage check
    try:
        memory_percent = psutil.virtual_memory().percent
        if memory_percent < 90:
            health_status["checks"]["memory"] = "healthy"
        else:
            health_status["checks"]["memory"] = f"warning: {memory_percent}% used"
            if memory_percent > 95:
                health_status["status"] = "unhealthy"
                logger.warning(f"High memory usage: {memory_percent}%")
    except Exception as e:
        health_status["checks"]["memory"] = "unknown"
        logger.warning(f"Could not check memory usage: {e}")
    
    # Disk space check
    try:
        disk_usage = psutil.disk_usage('/').percent
        if disk_usage < 90:
            health_status["checks"]["disk_space"] = "healthy"
        else:
            health_status["checks"]["disk_space"] = f"warning: {disk_usage}% used"
            if disk_usage > 95:
                health_status["status"] = "unhealthy"
                logger.warning(f"High disk usage: {disk_usage}%")
    except Exception as e:
        health_status["checks"]["disk_space"] = "unknown"
        logger.warning(f"Could not check disk usage: {e}")
    
    # Configuration check
    config_issues = []
    if not settings.secret_key or len(settings.secret_key) < 16:
        config_issues.append("weak_secret_key")
    if not settings.jwt_secret_key or len(settings.jwt_secret_key) < 16:
        config_issues.append("weak_jwt_key")
    
    if not config_issues:
        health_status["checks"]["configuration"] = "healthy"
    else:
        health_status["checks"]["configuration"] = f"issues: {', '.join(config_issues)}"
        if settings.is_production:
            health_status["status"] = "unhealthy"
            logger.error("Configuration issues detected", extra={
                'extra_fields': {
                    'issues': config_issues,
                    'event_type': 'config_validation_failed'
                }
            })
    
    # Log health check result
    if health_status["status"] == "healthy":
        logger.debug("Health check passed")
    else:
        logger.error("Health check failed", extra={
            'extra_fields': {
                'health_status': health_status,
                'event_type': 'health_check_failed'
            }
        })
    
    # Return appropriate HTTP status
    if health_status["status"] == "unhealthy":
        raise HTTPException(status_code=503, detail=health_status)
    
    return health_status


@app.get("/metrics")
async def get_metrics():
    """Get application metrics"""
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
    """Application information and configuration"""
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
    """User authentication"""
    username = form_data.username
    
    logger.info(f"Authentication attempt for user: {username}", extra={
        'extra_fields': {
            'username': username,
            'event_type': 'auth_attempt'
        }
    })
    
    user = authenticate_user(db, username, form_data.password)
    
    if not user:
        log_authentication_attempt(username, success=False)
        logger.warning(f"Failed authentication for user: {username}")
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    log_authentication_attempt(username, success=True)
    logger.info(f"Successful authentication for user: {username}", extra={
        'extra_fields': {
            'user_id': str(user.id),
            'username': username,
            'event_type': 'auth_success'
        }
    })
    
    access_token_expires = timedelta(minutes=settings.jwt_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/auth/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """Get current user information"""
    logger.debug(f"User profile accessed by: {current_user.username}", extra={
        'extra_fields': {
            'user_id': str(current_user.id),
            'username': current_user.username,
            'event_type': 'profile_access'
        }
    })
    
    return current_user


if __name__ == "__main__":
    uvicorn.run(
        "bookstore.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.is_development,
        log_level=settings.log_level.lower(),
        workers=1 if settings.is_development else settings.workers
    )