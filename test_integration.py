#!/usr/bin/env python3
"""
Simple test script to verify backend functionality
"""
import asyncio
import aiohttp
import json

async def test_backend():
    """Test the backend API endpoints"""
    base_url = "http://127.0.0.1:8000"
    
    async with aiohttp.ClientSession() as session:
        try:
            # Test health endpoint
            print("Testing health endpoint...")
            async with session.get(f"{base_url}/test") as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✓ Health check passed: {data}")
                else:
                    print(f"✗ Health check failed: {response.status}")
                    return
            
            # Test sources endpoint
            print("Testing sources endpoint...")
            async with session.get(f"{base_url}/api/v1/data/sources") as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✓ Sources check passed: Found {len(data.get('sources', []))} sources")
                    for source in data.get('sources', []):
                        print(f"  - {source['name']} ({source['type']}) - {source['status']}")
                else:
                    print(f"✗ Sources check failed: {response.status}")
                    return
            
            # Test chat endpoint
            print("Testing chat endpoint...")
            test_question = "What topics are covered in the documents?"
            async with session.post(f"{base_url}/api/v1/chat", 
                                  json={"question": test_question}) as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✓ Chat check passed")
                    print(f"Question: {test_question}")
                    print(f"Answer: {data.get('answer', 'No answer received')[:200]}...")
                else:
                    print(f"✗ Chat check failed: {response.status}")
                    error = await response.text()
                    print(f"Error: {error}")
            
        except Exception as e:
            print(f"✗ Backend test failed: {e}")

if __name__ == "__main__":
    print("Testing Backend Integration...")
    print("=" * 50)
    asyncio.run(test_backend())