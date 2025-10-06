#!/usr/bin/env python3
"""
Simple test script for the Media Monitoring Knowledge Assistant API
"""

import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:8000"

def test_health_endpoints():
    """Test health check endpoints"""
    print("Testing health endpoints...")
    
    # Test root endpoint
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"GET / - Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  Response: {json.dumps(data, indent=2)}")
        else:
            print(f"  Error: {response.text}")
    except Exception as e:
        print(f"  Error: {e}")
    
    # Test health endpoint
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"GET /health - Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  Response: {json.dumps(data, indent=2)}")
        else:
            print(f"  Error: {response.text}")
    except Exception as e:
        print(f"  Error: {e}")
    
    print()

def test_search_endpoint():
    """Test search endpoint"""
    print("Testing search endpoint...")
    
    search_data = {
        "query": "media monitoring strategies",
        "top_k": 3
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/search/",
            json=search_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"POST /search/ - Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  Response: {json.dumps(data, indent=2)}")
        else:
            print(f"  Error: {response.text}")
    except Exception as e:
        print(f"  Error: {e}")
    
    print()

def test_documents_endpoint():
    """Test documents listing endpoint"""
    print("Testing documents endpoint...")
    
    try:
        response = requests.get(f"{BASE_URL}/documents/")
        print(f"GET /documents/ - Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  Response: {json.dumps(data, indent=2)}")
        else:
            print(f"  Error: {response.text}")
    except Exception as e:
        print(f"  Error: {e}")
    
    print()

def test_openapi_docs():
    """Test OpenAPI documentation endpoints"""
    print("Testing OpenAPI documentation...")
    
    # Test OpenAPI JSON
    try:
        response = requests.get(f"{BASE_URL}/openapi.json")
        print(f"GET /openapi.json - Status: {response.status_code}")
        if response.status_code == 200:
            print("  OpenAPI specification available")
        else:
            print(f"  Error: {response.text}")
    except Exception as e:
        print(f"  Error: {e}")
    
    # Test Swagger UI
    try:
        response = requests.get(f"{BASE_URL}/docs")
        print(f"GET /docs - Status: {response.status_code}")
        if response.status_code == 200:
            print("  Swagger UI available")
        else:
            print(f"  Error: {response.text}")
    except Exception as e:
        print(f"  Error: {e}")
    
    print()

def test_error_handling():
    """Test error handling"""
    print("Testing error handling...")
    
    # Test invalid search query
    try:
        response = requests.post(
            f"{BASE_URL}/search/",
            json={"query": ""},  # Empty query should fail
            headers={"Content-Type": "application/json"}
        )
        print(f"POST /search/ (empty query) - Status: {response.status_code}")
        if response.status_code == 400:
            data = response.json()
            print(f"  Expected error: {json.dumps(data, indent=2)}")
        else:
            print(f"  Unexpected response: {response.text}")
    except Exception as e:
        print(f"  Error: {e}")
    
    # Test invalid top_k value
    try:
        response = requests.post(
            f"{BASE_URL}/search/",
            json={"query": "test", "top_k": 100},  # top_k > 50 should fail
            headers={"Content-Type": "application/json"}
        )
        print(f"POST /search/ (invalid top_k) - Status: {response.status_code}")
        if response.status_code == 422:  # Validation error
            print("  Expected validation error")
        else:
            print(f"  Response: {response.text}")
    except Exception as e:
        print(f"  Error: {e}")
    
    print()

def main():
    """Run all tests"""
    print("=" * 60)
    print("Media Monitoring Knowledge Assistant API Tests")
    print("=" * 60)
    print()
    
    # Wait a moment for server to start
    print("Waiting for server to be ready...")
    time.sleep(2)
    
    # Run tests
    test_health_endpoints()
    test_search_endpoint()
    test_documents_endpoint()
    test_openapi_docs()
    test_error_handling()
    
    print("=" * 60)
    print("Tests completed!")
    print("=" * 60)
    print()
    print("To view the interactive API documentation:")
    print(f"  Swagger UI: {BASE_URL}/docs")
    print(f"  ReDoc: {BASE_URL}/redoc")
    print()
    print("To test file upload, use the Swagger UI or curl:")
    print(f"  curl -X POST '{BASE_URL}/upload/' -F 'file=@your_document.pdf'")

if __name__ == "__main__":
    main()
