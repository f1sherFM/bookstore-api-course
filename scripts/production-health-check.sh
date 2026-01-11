#!/bin/bash

# BookStore API - Production Health Check Script
# Comprehensive health monitoring for production deployment

set -e

# Configuration
API_URL="${API_URL:-https://api.yourdomain.com}"
MONITORING_URL="${MONITORING_URL:-https://monitoring.yourdomain.com}"
SLACK_WEBHOOK="${SLACK_WEBHOOK:-}"
EMAIL_ALERT="${EMAIL_ALERT:-admin@yourdomain.com}"
TIMEOUT=30
RETRY_COUNT=3

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Logging
LOG_FILE="/var/log/bookstore-health-check.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

log() {
    echo -e "$1" | tee -a "$LOG_FILE"
}

log_info() {
    log "${BLUE}[$TIMESTAMP][INFO]${NC} $1"
}

log_success() {
    log "${GREEN}[$TIMESTAMP][SUCCESS]${NC} $1"
}

log_warning() {
    log "${YELLOW}[$TIMESTAMP][WARNING]${NC} $1"
}

log_error() {
    log "${RED}[$TIMESTAMP][ERROR]${NC} $1"
}

# Send alert function
send_alert() {
    local message="$1"
    local severity="$2"
    
    # Send Slack notification
    if [ -n "$SLACK_WEBHOOK" ]; then
        curl -X POST -H 'Content-type: application/json' \
            --data "{\"text\":\"🚨 BookStore API Alert [$severity]: $message\"}" \
            "$SLACK_WEBHOOK" &>/dev/null || true
    fi
    
    # Send email (requires mailutils)
    if command -v mail &> /dev/null && [ -n "$EMAIL_ALERT" ]; then
        echo "$message" | mail -s "BookStore API Alert [$severity]" "$EMAIL_ALERT" || true
    fi
    
    log_error "ALERT SENT: $message"
}

# Health check functions
check_api_health() {
    log_info "Checking API health endpoint..."
    
    local response
    local http_code
    
    for i in $(seq 1 $RETRY_COUNT); do
        response=$(curl -s -w "%{http_code}" --max-time $TIMEOUT "$API_URL/health" 2>/dev/null || echo "000")
        http_code="${response: -3}"
        
        if [ "$http_code" = "200" ]; then
            log_success "API health check passed (attempt $i)"
            return 0
        fi
        
        log_warning "API health check failed (attempt $i): HTTP $http_code"
        sleep 5
    done
    
    send_alert "API health endpoint is not responding (HTTP $http_code)" "CRITICAL"
    return 1
}

check_api_functionality() {
    log_info "Checking API functionality..."
    
    # Test books endpoint
    local response
    local http_code
    
    response=$(curl -s -w "%{http_code}" --max-time $TIMEOUT "$API_URL/api/v1/books/" 2>/dev/null || echo "000")
    http_code="${response: -3}"
    
    if [ "$http_code" = "200" ]; then
        log_success "API functionality check passed"
        return 0
    else
        send_alert "API functionality test failed (HTTP $http_code)" "HIGH"
        return 1
    fi
}

check_response_time() {
    log_info "Checking API response time..."
    
    local response_time
    response_time=$(curl -s -w "%{time_total}" -o /dev/null --max-time $TIMEOUT "$API_URL/health" 2>/dev/null || echo "999")
    
    # Convert to milliseconds
    response_time_ms=$(echo "$response_time * 1000" | bc -l 2>/dev/null || echo "999")
    response_time_ms=${response_time_ms%.*}  # Remove decimal part
    
    if [ "$response_time_ms" -lt 1000 ]; then
        log_success "Response time check passed: ${response_time_ms}ms"
        return 0
    elif [ "$response_time_ms" -lt 3000 ]; then
        log_warning "Response time is slow: ${response_time_ms}ms"
        return 0
    else
        send_alert "Response time is too slow: ${response_time_ms}ms" "MEDIUM"
        return 1
    fi
}

check_database_connectivity() {
    log_info "Checking database connectivity..."
    
    # The health endpoint should include database status
    local response
    response=$(curl -s --max-time $TIMEOUT "$API_URL/health" 2>/dev/null || echo "{}")
    
    # Check if response contains database status
    if echo "$response" | grep -q '"database".*"healthy"'; then
        log_success "Database connectivity check passed"
        return 0
    else
        send_alert "Database connectivity issue detected" "HIGH"
        return 1
    fi
}

check_ssl_certificate() {
    log_info "Checking SSL certificate..."
    
    local domain
    domain=$(echo "$API_URL" | sed 's|https://||' | sed 's|/.*||')
    
    # Check certificate expiry
    local cert_info
    cert_info=$(echo | openssl s_client -servername "$domain" -connect "$domain:443" 2>/dev/null | openssl x509 -noout -dates 2>/dev/null || echo "")
    
    if [ -n "$cert_info" ]; then
        local expiry_date
        expiry_date=$(echo "$cert_info" | grep "notAfter" | cut -d= -f2)
        
        # Check if certificate expires in next 30 days
        local expiry_timestamp
        local current_timestamp
        local days_until_expiry
        
        expiry_timestamp=$(date -d "$expiry_date" +%s 2>/dev/null || echo "0")
        current_timestamp=$(date +%s)
        days_until_expiry=$(( (expiry_timestamp - current_timestamp) / 86400 ))
        
        if [ "$days_until_expiry" -gt 30 ]; then
            log_success "SSL certificate check passed (expires in $days_until_expiry days)"
            return 0
        elif [ "$days_until_expiry" -gt 7 ]; then
            log_warning "SSL certificate expires soon (in $days_until_expiry days)"
            send_alert "SSL certificate expires in $days_until_expiry days" "MEDIUM"
            return 0
        else
            send_alert "SSL certificate expires very soon (in $days_until_expiry days)" "HIGH"
            return 1
        fi
    else
        send_alert "Could not check SSL certificate" "MEDIUM"
        return 1
    fi
}

check_disk_space() {
    log_info "Checking disk space..."
    
    local disk_usage
    disk_usage=$(df / | awk 'NR==2 {print $5}' | sed 's/%//')
    
    if [ "$disk_usage" -lt 80 ]; then
        log_success "Disk space check passed (${disk_usage}% used)"
        return 0
    elif [ "$disk_usage" -lt 90 ]; then
        log_warning "Disk space is getting low (${disk_usage}% used)"
        send_alert "Disk space is at ${disk_usage}%" "MEDIUM"
        return 0
    else
        send_alert "Disk space is critically low (${disk_usage}% used)" "HIGH"
        return 1
    fi
}

check_memory_usage() {
    log_info "Checking memory usage..."
    
    local memory_usage
    memory_usage=$(free | awk 'NR==2{printf "%.0f", $3*100/$2}')
    
    if [ "$memory_usage" -lt 80 ]; then
        log_success "Memory usage check passed (${memory_usage}% used)"
        return 0
    elif [ "$memory_usage" -lt 90 ]; then
        log_warning "Memory usage is high (${memory_usage}% used)"
        send_alert "Memory usage is at ${memory_usage}%" "MEDIUM"
        return 0
    else
        send_alert "Memory usage is critically high (${memory_usage}% used)" "HIGH"
        return 1
    fi
}

check_docker_containers() {
    log_info "Checking Docker containers..."
    
    if ! command -v docker &> /dev/null; then
        log_warning "Docker not available, skipping container check"
        return 0
    fi
    
    # Check if containers are running
    local containers
    containers=$(docker ps --format "table {{.Names}}\t{{.Status}}" | grep -E "(bookstore|postgres|redis|nginx)" || echo "")
    
    if [ -n "$containers" ]; then
        local unhealthy_containers
        unhealthy_containers=$(echo "$containers" | grep -v "Up" || echo "")
        
        if [ -z "$unhealthy_containers" ]; then
            log_success "All Docker containers are running"
            return 0
        else
            send_alert "Some Docker containers are not healthy: $unhealthy_containers" "HIGH"
            return 1
        fi
    else
        log_warning "No BookStore containers found"
        return 1
    fi
}

check_log_errors() {
    log_info "Checking for recent errors in logs..."
    
    # Check for errors in the last 5 minutes
    local error_count
    error_count=$(journalctl -u bookstore-api --since "5 minutes ago" | grep -i error | wc -l 2>/dev/null || echo "0")
    
    if [ "$error_count" -eq 0 ]; then
        log_success "No recent errors found in logs"
        return 0
    elif [ "$error_count" -lt 10 ]; then
        log_warning "Found $error_count errors in recent logs"
        return 0
    else
        send_alert "High error rate detected: $error_count errors in last 5 minutes" "HIGH"
        return 1
    fi
}

# Main health check function
run_health_checks() {
    log_info "🏥 Starting comprehensive health check for BookStore API..."
    echo
    
    local total_checks=0
    local passed_checks=0
    local failed_checks=0
    
    # List of health check functions
    local checks=(
        "check_api_health"
        "check_api_functionality"
        "check_response_time"
        "check_database_connectivity"
        "check_ssl_certificate"
        "check_disk_space"
        "check_memory_usage"
        "check_docker_containers"
        "check_log_errors"
    )
    
    # Run all checks
    for check in "${checks[@]}"; do
        total_checks=$((total_checks + 1))
        
        if $check; then
            passed_checks=$((passed_checks + 1))
        else
            failed_checks=$((failed_checks + 1))
        fi
        
        echo
    done
    
    # Summary
    log_info "📊 Health Check Summary:"
    log_info "Total checks: $total_checks"
    log_success "Passed: $passed_checks"
    
    if [ "$failed_checks" -gt 0 ]; then
        log_error "Failed: $failed_checks"
        
        # Send summary alert if there are failures
        send_alert "Health check completed with $failed_checks failures out of $total_checks checks" "SUMMARY"
        
        return 1
    else
        log_success "All health checks passed! ✅"
        return 0
    fi
}

# Generate health report
generate_report() {
    local report_file="/tmp/bookstore-health-report-$(date +%Y%m%d-%H%M%S).json"
    
    log_info "Generating health report..."
    
    cat > "$report_file" << EOF
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "api_url": "$API_URL",
  "monitoring_url": "$MONITORING_URL",
  "checks": {
    "api_health": "$(check_api_health &>/dev/null && echo "PASS" || echo "FAIL")",
    "api_functionality": "$(check_api_functionality &>/dev/null && echo "PASS" || echo "FAIL")",
    "response_time": "$(check_response_time &>/dev/null && echo "PASS" || echo "FAIL")",
    "database": "$(check_database_connectivity &>/dev/null && echo "PASS" || echo "FAIL")",
    "ssl_certificate": "$(check_ssl_certificate &>/dev/null && echo "PASS" || echo "FAIL")",
    "disk_space": "$(check_disk_space &>/dev/null && echo "PASS" || echo "FAIL")",
    "memory_usage": "$(check_memory_usage &>/dev/null && echo "PASS" || echo "FAIL")",
    "docker_containers": "$(check_docker_containers &>/dev/null && echo "PASS" || echo "FAIL")",
    "log_errors": "$(check_log_errors &>/dev/null && echo "PASS" || echo "FAIL")"
  },
  "system_info": {
    "hostname": "$(hostname)",
    "uptime": "$(uptime -p 2>/dev/null || uptime)",
    "load_average": "$(uptime | awk -F'load average:' '{print $2}' | xargs)",
    "disk_usage": "$(df -h / | awk 'NR==2 {print $5}')",
    "memory_usage": "$(free -h | awk 'NR==2{printf "%s/%s (%.0f%%)", $3,$2,$3*100/$2}')"
  }
}
EOF
    
    log_success "Health report generated: $report_file"
    echo "$report_file"
}

# Main script logic
case "${1:-check}" in
    "check")
        run_health_checks
        ;;
    "report")
        generate_report
        ;;
    "monitor")
        log_info "Starting continuous monitoring (press Ctrl+C to stop)..."
        while true; do
            run_health_checks
            sleep 300  # Check every 5 minutes
        done
        ;;
    "test")
        log_info "Running test health check (no alerts)..."
        SLACK_WEBHOOK=""
        EMAIL_ALERT=""
        run_health_checks
        ;;
    *)
        echo "Usage: $0 {check|report|monitor|test}"
        echo
        echo "Commands:"
        echo "  check   - Run health checks once (default)"
        echo "  report  - Generate detailed health report"
        echo "  monitor - Run continuous monitoring"
        echo "  test    - Run health checks without sending alerts"
        echo
        echo "Environment variables:"
        echo "  API_URL         - API base URL (default: https://api.yourdomain.com)"
        echo "  MONITORING_URL  - Monitoring URL (default: https://monitoring.yourdomain.com)"
        echo "  SLACK_WEBHOOK   - Slack webhook URL for alerts"
        echo "  EMAIL_ALERT     - Email address for alerts"
        exit 1
        ;;
esac