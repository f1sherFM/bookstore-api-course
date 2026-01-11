#!/usr/bin/env python3
"""
Create test data via API
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def create_test_data():
    """Create test data via API"""
    print("🔧 Creating test data via API...")
    
    # 1. Create regular user
    print("👤 Creating user...")
    user_data = {
        "email": "user@example.com",
        "username": "testuser",
        "full_name": "Test User",
        "password": "password123",
        "is_active": True
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/users/", json=user_data)
    if response.status_code == 201:
        print("✅ User created")
        user = response.json()
    else:
        print(f"❌ User creation error: {response.status_code}")
        print(response.text)
        return
    
    # 2. Login to system
    print("🔐 Logging in...")
    login_data = {
        "username": "testuser",
        "password": "password123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
    if response.status_code == 200:
        token_data = response.json()
        token = token_data["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        print("✅ Successful login")
    else:
        print(f"❌ Login error: {response.status_code}")
        print(response.text)
        return
    
    # Check if data already exists
    response = requests.get(f"{BASE_URL}/api/v1/books/")
    if response.status_code == 200 and len(response.json()) > 0:
        print("📚 Books already exist")
        return
    
    print("📚 Data will be created by administrator...")
    print("Creating books requires superuser privileges")
    print("Use admin panel or create superuser")

if __name__ == "__main__":
    try:
        create_test_data()
    except requests.exceptions.ConnectionError:
        print("❌ API unavailable. Start server with: python run_bookstore.py")