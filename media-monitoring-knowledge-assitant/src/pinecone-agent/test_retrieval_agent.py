#!/usr/bin/env python3
"""
Test script for the retrieval agent
"""

import os
import sys
from pathlib import Path

# Add the src directory to Python path
sys.path.append(str(Path(__file__).parent / "src"))

from retriver_agent import run_retrieval_agent

def test_retrieval_agent():
    """Test the retrieval agent with various queries"""
    
    print("🚀 Testing Retrieval Agent")
    print("=" * 50)
    
    # Test 1: List available documents
    print("\n📋 Test 1: Listing available documents")
    try:
        response = run_retrieval_agent("List all available documents in the knowledge base")
        print(f"✅ Response: {response}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Add document
    print("\n📄 Test 2: Adding document to vector store")
    try:
        response = run_retrieval_agent("Add the SampleRadioPSAScripts.pdf document to the vector database")
        print(f"✅ Response: {response}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: Search query
    print("\n🔍 Test 3: Searching vector database")
    try:
        response = run_retrieval_agent("Search for information about radio PSA scripts in the vector database")
        print(f"✅ Response: {response}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 4: General query
    print("\n💬 Test 4: General conversation")
    try:
        response = run_retrieval_agent("Hello! How can you help me with document management?")
        print(f"✅ Response: {response}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    # Check if environment variables are set
    required_vars = ["GEMINI_API_KEY", "ASTRA_DB_APPLICATION_TOKEN", "ASTRA_DB_API_ENDPOINT"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"⚠️  Missing environment variables: {', '.join(missing_vars)}")
        print("Please set these in your .env file")
        sys.exit(1)
    
    test_retrieval_agent()
