# 🐳 Docker Setup for BookStore API

## Overview

Complete containerization of BookStore API using Docker and docker-compose for local development and production deployment.

## File Structure

```
├── Dockerfile              # Multi-stage Docker build
├── docker-compose.yml      # Local development
├── config/nginx.conf       # Reverse proxy configuration
├── database/init.sql       # PostgreSQL initialization
├── .dockerignore           # Docker build exclusions
├── .env.example            # Environment variables example
└── docker-build.sh         # Build script (Linux/Mac)
```

## Quick Start

### 1. Environment Setup

```bash
# Copy example configuration
cp .env.example .env

# Edit environment variables
nano .env
```

### 2. Build and Run

```bash
# Build image
docker build -t bookstore-api:latest .

# Start all services
docker-compose up -d

# Check status
docker-compose ps
```

### 3. Health Check

```bash
# Health check
curl http://localhost:8000/health

# API documentation
open http://localhost:8000/docs

# Through Nginx (port 80)
curl http://localhost/health
```

## Container Architecture

### API Container (bookstore-api)
- **Base Image**: python:3.11-slim
- **Multi-stage build** for size optimization
- **Non-root user** for security
- **Health check** built into container
- **Port**: 8000

### Database Container (PostgreSQL)
- **Image**: postgres:15-alpine
- **Persistent storage** via Docker volumes
- **Health check** with pg_isready
- **Port**: 5432

### Cache Container (Redis)
- **Image**: redis:7-alpine
- **Persistent storage** with AOF
- **Health check** with redis-cli ping
- **Port**: 6379

### Reverse Proxy (Nginx)
- **Image**: nginx:alpine
- **Rate limiting** configured
- **Security headers** added
- **Gzip compression** enabled
- **Ports**: 80, 443

## Docker Image Features

### Multi-stage Build
```dockerfile
# Stage 1: Builder - installs dependencies
FROM python:3.11-slim as builder
# ... install dependencies in venv

# Stage 2: Production - runtime only
FROM python:3.11-slim as production
# ... copy venv and application
```

### Security
- ✅ Non-root user
- ✅ Minimal base image
- ✅ Only necessary dependencies
- ✅ Health check for monitoring

### Optimization
- ✅ .dockerignore for excluding unnecessary files
- ✅ Docker layer caching
- ✅ Python virtual environment
- ✅ Compression in Nginx

## Management Commands

### Development
```bash
# Start in development mode
docker-compose up

# Rebuild after changes
docker-compose up --build

# View logs
docker-compose logs -f api

# Connect to container
docker-compose exec api bash
```

### Production
```bash
# Build production image
docker build --target production -t bookstore-api:prod .

# Run with production configuration
docker run -d \
  --name bookstore-api \
  -p 8000:8000 \
  --env-file .env.production \
  bookstore-api:prod
```

### Monitoring
```bash
# Container status
docker-compose ps

# Resource usage
docker stats

# Health check
docker-compose exec api curl http://localhost:8000/health
```

## Environment Variables

### Required
- `DATABASE_URL` - PostgreSQL connection URL
- `SECRET_KEY` - Application secret key
- `JWT_SECRET_KEY` - JWT token key

### Optional
- `REDIS_URL` - Redis connection URL (default: redis://localhost:6379)
- `LOG_LEVEL` - Logging level (default: INFO)
- `ENVIRONMENT` - Environment (development/staging/production)

## Volumes and Data

### Persistent Storage
- `postgres_data` - PostgreSQL data
- `redis_data` - Redis data
- `./logs` - Application logs

### Backup
```bash
# Backup PostgreSQL
docker-compose exec db pg_dump -U bookstore bookstore_db > backup.sql

# Restore PostgreSQL
docker-compose exec -T db psql -U bookstore bookstore_db < backup.sql
```

## Troubleshooting

### Startup Issues
```bash
# Check logs
docker-compose logs api

# Check health check
docker-compose exec api curl http://localhost:8000/health

# Restart services
docker-compose restart
```

### Database Issues
```bash
# Check database connection
docker-compose exec api python -c "
from bookstore.database import engine
print(engine.execute('SELECT 1').scalar())
"

# Recreate database
docker-compose down -v
docker-compose up -d
```

## Production Deployment

### Docker Registry
```bash
# Tag for registry
docker tag bookstore-api:latest your-registry.com/bookstore-api:v1.0.0

# Push to registry
docker push your-registry.com/bookstore-api:v1.0.0
```

### Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: bookstore-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: bookstore-api
  template:
    metadata:
      labels:
        app: bookstore-api
    spec:
      containers:
      - name: api
        image: your-registry.com/bookstore-api:v1.0.0
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: bookstore-secrets
              key: database-url
```

## Metrics and Monitoring

### Health Check Response
```json
{
  "status": "healthy",
  "timestamp": "2024-01-10T10:00:00Z",
  "version": "1.0.0",
  "service": "bookstore-api",
  "checks": {
    "database": "healthy",
    "memory": "healthy",
    "disk_space": "healthy",
    "environment": "healthy"
  }
}
```

### Prometheus Metrics
- Available through `/metrics` endpoint
- Include application and system metrics
- Grafana integration for visualization

## Next Steps

1. ✅ **Docker containerization** - completed
2. 🔄 **Environment Configuration** - in progress
3. ⏳ **CI/CD Pipeline** - next stage
4. ⏳ **Monitoring & Logging** - planned
5. ⏳ **Cloud Deployment** - final stage