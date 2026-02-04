import requests
import json
import uuid
from datetime import datetime, timedelta
import jwt

# Create a mock JWT token for testing (this is just for testing purposes)
SECRET_KEY = "test-secret-key-change-in-production"
ALGORITHM = "HS256"

def create_mock_token(user_id: str):
    """Create a mock JWT token for testing"""
    payload = {
        "sub": user_id,
        "exp": datetime.utcnow() + timedelta(hours=1),
        "iat": datetime.utcnow()
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def test_endpoints():
    base_url = "http://localhost:8000"

    # Create a mock user ID and token
    user_id = "test-user-123"
    token = create_mock_token(user_id)

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    print("Testing endpoints with mock JWT token...")

    # Test 1: GET /api/v1/{user_id}/tasks (should return empty list initially)
    print("\n1. Testing GET /api/v1/{user_id}/tasks")
    try:
        response = requests.get(f"{base_url}/api/v1/{user_id}/tasks", headers=headers)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")

    # Test 2: POST /api/v1/{user_id}/tasks (create a new task)
    print("\n2. Testing POST /api/v1/{user_id}/tasks")
    task_data = {
        "title": "Test Task from Endpoint Test",
        "description": "This is a test task created via API"
    }
    try:
        response = requests.post(f"{base_url}/api/v1/{user_id}/tasks",
                                headers=headers,
                                json=task_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 201:
            task = response.json()
            print(f"   Created task: {task['title']}")
            task_id = task['id']  # Save for later tests
        else:
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")

    # Test 3: GET /api/v1/{user_id}/tasks (should return the created task)
    print("\n3. Testing GET /api/v1/{user_id}/tasks again")
    try:
        response = requests.get(f"{base_url}/api/v1/{user_id}/tasks", headers=headers)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")

    # Test 4: GET /api/v1/{user_id}/tasks/{task_id} (get specific task)
    print("\n4. Testing GET /api/v1/{user_id}/tasks/{task_id}")
    try:
        # Use a dummy UUID for now since we don't have the real one from the response
        # In a real scenario we'd use the task_id from the POST response
        response = requests.get(f"{base_url}/api/v1/{user_id}/tasks/{uuid.uuid4()}", headers=headers)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")

    # Test 5: Health check
    print("\n5. Testing health endpoint")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")

    print("\nEndpoint testing completed!")

if __name__ == "__main__":
    test_endpoints()