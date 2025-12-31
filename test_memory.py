"""
Test script to demonstrate the chatbot memory functionality.
Run the FastAPI server first: python main.py
Then run this script: python test_memory.py
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_memory():
    print("=" * 60)
    print("Testing AI Agent Memory Functionality")
    print("=" * 60)
    
    # Test 1: Start a new conversation
    print("\n1. Starting a new conversation...")
    response = requests.post(f"{BASE_URL}/new-conversation")
    data = response.json()
    thread_id = data["thread_id"]
    print(f"   Thread ID: {thread_id}")
    
    # Test 2: Send first message
    print("\n2. Sending first message: 'My name is Alice'")
    response = requests.post(
        f"{BASE_URL}/chat",
        json={"message": "My name is Alice", "thread_id": thread_id}
    )
    data = response.json()
    print(f"   AI Response: {data['response']}")
    
    # Test 3: Send second message to test memory
    print("\n3. Testing memory: 'What is my name?'")
    response = requests.post(
        f"{BASE_URL}/chat",
        json={"message": "What is my name?", "thread_id": thread_id}
    )
    data = response.json()
    print(f"   AI Response: {data['response']}")
    
    # Test 4: Get conversation history
    print("\n4. Retrieving conversation history...")
    response = requests.post(
        f"{BASE_URL}/history",
        json={"thread_id": thread_id}
    )
    data = response.json()
    print(f"   Total messages: {len(data['messages'])}")
    for i, msg in enumerate(data['messages'], 1):
        print(f"   Message {i} ({msg['type']}): {msg['content'][:50]}...")
    
    # Test 5: Test with new thread (should not remember)
    print("\n5. Starting new conversation (different thread)...")
    response = requests.post(
        f"{BASE_URL}/chat",
        json={"message": "What is my name?"}
    )
    data = response.json()
    new_thread_id = data['thread_id']
    print(f"   New Thread ID: {new_thread_id}")
    print(f"   AI Response: {data['response']}")
    print(f"   (Should NOT remember Alice)")
    
    print("\n" + "=" * 60)
    print("Memory test completed!")
    print("=" * 60)

if __name__ == "__main__":
    try:
        test_memory()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API server.")
        print("Make sure the server is running: python main.py")
    except Exception as e:
        print(f"Error: {e}")
