#!/usr/bin/env python3
"""
Simple test script to verify backend API functionality
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_health():
    """Test basic health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/test")
        print(f"Health check: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_sources():
    """Test sources endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/api/v1/data/sources")
        print(f"Sources check: {response.status_code}")
        data = response.json()
        print(f"Found {len(data.get('sources', []))} sources")
        for source in data.get('sources', []):
            print(f"  - {source.get('name')} ({source.get('type')}) - {source.get('status')}")
        return response.status_code == 200
    except Exception as e:
        print(f"Sources check failed: {e}")
        return False

def test_chat():
    """Test chat endpoint"""
    try:
        test_question = "What topics are covered in the uploaded documents?"
        response = requests.post(
            f"{BASE_URL}/api/v1/chat",
            json={"question": test_question},
            headers={"Content-Type": "application/json"}
        )
        print(f"Chat check: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Question: {test_question}")
            print(f"Answer: {data.get('answer', 'No answer received')}")
        else:
            print(f"Error response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Chat check failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Testing Backend API...")
    print("=" * 50)
    
    tests = [
        ("Health Check", test_health),
        ("Sources Check", test_sources),
        ("Chat Check", test_chat)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 20)
        success = test_func()
        results.append((test_name, success))
        print(f"Result: {'✓ PASSED' if success else '✗ FAILED'}")
    
    print("\n" + "=" * 50)
    print("SUMMARY:")
    for test_name, success in results:
        status = "✓ PASSED" if success else "✗ FAILED"
        print(f"{test_name}: {status}")

if __name__ == "__main__":
    main()