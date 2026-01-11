#!/bin/bash

# BookStore API - Project Validation Script
# This script validates that the project is properly organized for GitHub publication

set -e

echo "🔍 BookStore API - Project Validation"
echo "====================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Validation functions
validate_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✅${NC} $1"
        return 0
    else
        echo -e "${RED}❌${NC} $1 (missing)"
        return 1
    fi
}

validate_directory() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✅${NC} $1/"
        return 0
    else
        echo -e "${RED}❌${NC} $1/ (missing)"
        return 1
    fi
}

validate_executable() {
    if [ -x "$1" ]; then
        echo -e "${GREEN}✅${NC} $1 (executable)"
        return 0
    else
        echo -e "${YELLOW}⚠️${NC} $1 (not executable)"
        return 1
    fi
}

# Initialize counters
PASSED=0
FAILED=0

echo -e "\n${BLUE}📁 Core Project Structure${NC}"
echo "========================="

# Essential files
files=(
    "README.md"
    "LICENSE"
    "CHANGELOG.md"
    "CONTRIBUTING.md"
    "Makefile"
    "Dockerfile"
    "docker-compose.yml"
    "docker-compose.prod.yml"
    "requirements.txt"
    "pyproject.toml"
    ".gitignore"
    ".env.example"
)

for file in "${files[@]}"; do
    if validate_file "$file"; then
        ((PASSED++))
    else
        ((FAILED++))
    fi
done

echo -e "\n${BLUE}📁 Directory Structure${NC}"
echo "======================"

# Essential directories
directories=(
    "bookstore"
    "tests"
    "docs"
    "examples"
    "scripts"
    "k8s"
    "grafana"
    ".github"
    ".github/workflows"
)

for dir in "${directories[@]}"; do
    if validate_directory "$dir"; then
        ((PASSED++))
    else
        ((FAILED++))
    fi
done

echo -e "\n${BLUE}🐍 Python Package Structure${NC}"
echo "============================"

# Python package files
python_files=(
    "bookstore/__init__.py"
    "bookstore/main.py"
    "bookstore/models.py"
    "bookstore/schemas.py"
    "bookstore/auth.py"
    "bookstore/database.py"
    "bookstore/config.py"
    "bookstore/logging_config.py"
    "bookstore/middleware.py"
    "run_bookstore.py"
)

for file in "${python_files[@]}"; do
    if validate_file "$file"; then
        ((PASSED++))
    else
        ((FAILED++))
    fi
done

echo -e "\n${BLUE}🧪 Testing Framework${NC}"
echo "===================="

# Test files
test_files=(
    "tests/__init__.py"
    "tests/conftest.py"
    "tests/test_unit_basic.py"
    "tests/test_api_integration.py"
    "tests/test_property_based.py"
    "tests/test_performance.py"
    "tests/factories.py"
    "tests/locustfile.py"
    "pytest.ini"
)

for file in "${test_files[@]}"; do
    if validate_file "$file"; then
        ((PASSED++))
    else
        ((FAILED++))
    fi
done

echo -e "\n${BLUE}🚀 CI/CD Pipeline${NC}"
echo "=================="

# CI/CD files
cicd_files=(
    ".github/workflows/ci.yml"
    ".github/workflows/dependencies.yml"
    ".github/workflows/performance.yml"
    ".github/ISSUE_TEMPLATE/bug_report.md"
    ".github/ISSUE_TEMPLATE/feature_request.md"
    ".github/pull_request_template.md"
)

for file in "${cicd_files[@]}"; do
    if validate_file "$file"; then
        ((PASSED++))
    else
        ((FAILED++))
    fi
done

echo -e "\n${BLUE}☸️ Kubernetes Deployment${NC}"
echo "========================="

# Kubernetes files
k8s_files=(
    "k8s/namespace.yaml"
    "k8s/configmap.yaml"
    "k8s/secrets.yaml"
    "k8s/postgresql.yaml"
    "k8s/redis.yaml"
    "k8s/api-deployment.yaml"
    "k8s/ingress.yaml"
    "k8s/monitoring.yaml"
)

for file in "${k8s_files[@]}"; do
    if validate_file "$file"; then
        ((PASSED++))
    else
        ((FAILED++))
    fi
done

echo -e "\n${BLUE}🔧 Scripts & Tools${NC}"
echo "=================="

# Scripts
scripts=(
    "scripts/setup-dev.sh"
    "scripts/production-health-check.sh"
    "k8s/deploy.sh"
)

for script in "${scripts[@]}"; do
    if validate_executable "$script"; then
        ((PASSED++))
    else
        ((FAILED++))
    fi
done

echo -e "\n${BLUE}📚 Documentation${NC}"
echo "=================="

# Documentation files
doc_files=(
    "docs/PROJECT_STRUCTURE.md"
    "docs/PRODUCTION_DEPLOYMENT.md"
    "docs/DOCKER_SETUP.md"
    "docs/CI_CD_SETUP.md"
    "docs/TESTING_SUMMARY.md"
)

for file in "${doc_files[@]}"; do
    if validate_file "$file"; then
        ((PASSED++))
    else
        ((FAILED++))
    fi
done

echo -e "\n${BLUE}📊 Monitoring & Configuration${NC}"
echo "=============================="

# Configuration files
config_files=(
    "prometheus.yml"
    "loki.yml"
    "promtail.yml"
    "redis.conf"
    "nginx.conf"
    "nginx-prod.conf"
    "grafana/dashboards/bookstore-api.json"
)

for file in "${config_files[@]}"; do
    if validate_file "$file"; then
        ((PASSED++))
    else
        ((FAILED++))
    fi
done

echo -e "\n${BLUE}🔍 Code Quality Checks${NC}"
echo "======================"

# Check if Python is available
if command -v python3 &> /dev/null; then
    echo -e "${GREEN}✅${NC} Python 3 available"
    ((PASSED++))
else
    echo -e "${RED}❌${NC} Python 3 not available"
    ((FAILED++))
fi

# Check if Docker is available
if command -v docker &> /dev/null; then
    echo -e "${GREEN}✅${NC} Docker available"
    ((PASSED++))
else
    echo -e "${YELLOW}⚠️${NC} Docker not available"
    ((FAILED++))
fi

# Check if make is available
if command -v make &> /dev/null; then
    echo -e "${GREEN}✅${NC} Make available"
    ((PASSED++))
else
    echo -e "${YELLOW}⚠️${NC} Make not available"
    ((FAILED++))
fi

echo -e "\n${BLUE}📋 Validation Summary${NC}"
echo "====================="

TOTAL=$((PASSED + FAILED))
PERCENTAGE=$((PASSED * 100 / TOTAL))

echo -e "Total checks: ${BLUE}$TOTAL${NC}"
echo -e "Passed: ${GREEN}$PASSED${NC}"
echo -e "Failed: ${RED}$FAILED${NC}"
echo -e "Success rate: ${GREEN}$PERCENTAGE%${NC}"

if [ $FAILED -eq 0 ]; then
    echo -e "\n${GREEN}🎉 PROJECT VALIDATION SUCCESSFUL!${NC}"
    echo -e "${GREEN}✅ Your BookStore API project is ready for GitHub publication!${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Create a new GitHub repository"
    echo "2. Push your code: git push origin main"
    echo "3. Configure GitHub secrets for CI/CD"
    echo "4. Deploy to your preferred environment"
    exit 0
elif [ $FAILED -le 3 ]; then
    echo -e "\n${YELLOW}⚠️ PROJECT VALIDATION MOSTLY SUCCESSFUL${NC}"
    echo -e "${YELLOW}Minor issues found, but project is ready for GitHub${NC}"
    exit 0
else
    echo -e "\n${RED}❌ PROJECT VALIDATION FAILED${NC}"
    echo -e "${RED}Please fix the missing files/directories before publishing${NC}"
    exit 1
fi