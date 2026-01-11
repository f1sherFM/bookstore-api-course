#!/bin/bash

# BookStore API Database Backup Script
# Runs automated backups with rotation

set -e

# Configuration
BACKUP_DIR="/backups"
DB_HOST="db"
DB_PORT="5432"
DB_NAME="${POSTGRES_DB}"
DB_USER="${POSTGRES_USER}"
PGPASSWORD="${POSTGRES_PASSWORD}"
RETENTION_DAYS=30
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/bookstore_backup_${DATE}.sql"

# Create backup directory if it doesn't exist
mkdir -p "${BACKUP_DIR}"

echo "🗄️ Starting database backup..."
echo "Database: ${DB_NAME}"
echo "Host: ${DB_HOST}"
echo "Backup file: ${BACKUP_FILE}"

# Wait for database to be ready
echo "⏳ Waiting for database to be ready..."
until pg_isready -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" -d "${DB_NAME}"; do
  echo "Database is not ready yet. Waiting..."
  sleep 5
done

echo "✅ Database is ready. Starting backup..."

# Create backup
export PGPASSWORD
pg_dump -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" -d "${DB_NAME}" \
  --verbose \
  --no-password \
  --format=custom \
  --compress=9 \
  --file="${BACKUP_FILE}.custom"

# Also create SQL dump for easier inspection
pg_dump -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" -d "${DB_NAME}" \
  --verbose \
  --no-password \
  --format=plain \
  --file="${BACKUP_FILE}"

# Compress SQL dump
gzip "${BACKUP_FILE}"

echo "✅ Backup completed successfully!"
echo "Files created:"
echo "  - ${BACKUP_FILE}.custom (PostgreSQL custom format)"
echo "  - ${BACKUP_FILE}.gz (SQL dump, compressed)"

# Get backup sizes
CUSTOM_SIZE=$(du -h "${BACKUP_FILE}.custom" | cut -f1)
SQL_SIZE=$(du -h "${BACKUP_FILE}.gz" | cut -f1)

echo "Backup sizes:"
echo "  - Custom format: ${CUSTOM_SIZE}"
echo "  - SQL dump: ${SQL_SIZE}"

# Cleanup old backups
echo "🧹 Cleaning up old backups (older than ${RETENTION_DAYS} days)..."
find "${BACKUP_DIR}" -name "bookstore_backup_*.sql*" -type f -mtime +${RETENTION_DAYS} -delete
find "${BACKUP_DIR}" -name "bookstore_backup_*.custom" -type f -mtime +${RETENTION_DAYS} -delete

# List remaining backups
echo "📋 Current backups:"
ls -lh "${BACKUP_DIR}"/bookstore_backup_* 2>/dev/null || echo "No backups found"

# Test backup integrity
echo "🔍 Testing backup integrity..."
pg_restore --list "${BACKUP_FILE}.custom" > /dev/null
echo "✅ Backup integrity check passed"

# Create backup metadata
cat > "${BACKUP_FILE}.meta" << EOF
{
  "backup_date": "${DATE}",
  "database": "${DB_NAME}",
  "host": "${DB_HOST}",
  "user": "${DB_USER}",
  "format": "custom",
  "compression": "9",
  "size_custom": "${CUSTOM_SIZE}",
  "size_sql": "${SQL_SIZE}",
  "retention_days": ${RETENTION_DAYS}
}
EOF

echo "📊 Backup metadata saved to ${BACKUP_FILE}.meta"
echo "🎉 Backup process completed successfully!"

# Optional: Send notification (uncomment if needed)
# curl -X POST "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK" \
#   -H 'Content-type: application/json' \
#   --data "{\"text\":\"✅ BookStore DB backup completed: ${BACKUP_FILE}\"}"