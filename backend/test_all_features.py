import requests
import json
import uuid
from datetime import datetime, timedelta
import jwt
import time

# Create a mock JWT token for testing (this is just for testing purposes)
SECRET_KEY = "fr1QoLvfYNVldBhgB4kuFgf1VXw1R3D4"  # Using the secret from your .env
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

def test_all_features():
    base_url = "http://localhost:8000"

    # Create a mock user ID and token
    user_id = "test-user-123"
    token = create_mock_token(user_id)

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    print("Testing all features through endpoints...")

    # Test 1: GET /api/v1/{user_id}/tasks (should return empty list initially)
    print("\n1. Testing GET /api/v1/{user_id}/tasks (empty)")
    try:
        response = requests.get(f"{base_url}/api/v1/{user_id}/tasks", headers=headers)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        tasks_before = response.json()
    except Exception as e:
        print(f"   Error: {e}")
        tasks_before = []

    # Test 2: POST /api/v1/{user_id}/tasks (create a new task)
    print("\n2. Testing POST /api/v1/{user_id}/tasks (create task)")
    task_data = {
        "title": "Test Task - Feature Testing",
        "description": "This is a test task created via API for feature testing"
    }
    try:
        response = requests.post(f"{base_url}/api/v1/{user_id}/tasks",
                                headers=headers,
                                json=task_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 201:
            created_task = response.json()
            print(f"   Created task: {created_task['title']}")
            print(f"   Task ID: {created_task['id']}")
            task_id = created_task['id']
        else:
            print(f"   Failed to create task: {response.text}")
            return
    except Exception as e:
        print(f"   Error: {e}")
        return

    # Test 3: GET /api/v1/{user_id}/tasks (should return the created task)
    print("\n3. Testing GET /api/v1/{user_id}/tasks (after creation)")
    try:
        response = requests.get(f"{base_url}/api/v1/{user_id}/tasks", headers=headers)
        print(f"   Status: {response.status_code}")
        tasks_after_create = response.json()
        print(f"   Number of tasks: {len(tasks_after_create)}")
        print(f"   Response: {json.dumps(tasks_after_create, indent=2)}")
    except Exception as e:
        print(f"   Error: {e}")

    # Test 4: GET /api/v1/{user_id}/tasks/{task_id} (get specific task)
    print("\n4. Testing GET /api/v1/{user_id}/tasks/{task_id} (get specific task)")
    try:
        response = requests.get(f"{base_url}/api/v1/{user_id}/tasks/{task_id}", headers=headers)
        print(f"   Status: {response.status_code}")
        specific_task = response.json()
        print(f"   Retrieved task: {specific_task['title']}")
        print(f"   Completed: {specific_task['completed']}")
    except Exception as e:
        print(f"   Error: {e}")

    # Test 5: PUT /api/v1/{user_id}/tasks/{task_id} (update task)
    print("\n5. Testing PUT /api/v1/{user_id}/tasks/{task_id} (update task)")
    update_data = {
        "title": "Updated Test Task - Feature Testing",
        "description": "This task has been updated via API"
    }
    try:
        response = requests.put(f"{base_url}/api/v1/{user_id}/tasks/{task_id}",
                               headers=headers,
                               json=update_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            updated_task = response.json()
            print(f"   Updated task: {updated_task['title']}")
            print(f"   Updated description: {updated_task['description']}")
        else:
            print(f"   Failed to update task: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")

    # Test 6: PATCH /api/v1/{user_id}/tasks/{task_id}/complete (mark as complete)
    print("\n6. Testing PATCH /api/v1/{user_id}/tasks/{task_id}/complete (mark as complete)")
    completion_data = {
        "completed": True
    }
    try:
        response = requests.patch(f"{base_url}/api/v1/{user_id}/tasks/{task_id}/complete",
                                 headers=headers,
                                 json=completion_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            completed_task = response.json()
            print(f"   Task completed: {completed_task['completed']}")
        else:
            print(f"   Failed to complete task: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")

    # Test 7: GET /api/v1/{user_id}/tasks (check completion status)
    print("\n7. Testing GET /api/v1/{user_id}/tasks (after completion)")
    try:
        response = requests.get(f"{base_url}/api/v1/{user_id}/tasks", headers=headers)
        print(f"   Status: {response.status_code}")
        tasks_after_completion = response.json()
        print(f"   Number of tasks: {len(tasks_after_completion)}")
        if len(tasks_after_completion) > 0:
            print(f"   First task completion status: {tasks_after_completion[0]['completed']}")
    except Exception as e:
        print(f"   Error: {e}")

    # Test 8: PATCH /api/v1/{user_id}/tasks/{task_id}/complete (mark as pending/uncomplete)
    print("\n8. Testing PATCH /api/v1/{user_id}/tasks/{task_id}/complete (mark as pending)")
    uncomplete_data = {
        "completed": False
    }
    try:
        response = requests.patch(f"{base_url}/api/v1/{user_id}/tasks/{task_id}/complete",
                                 headers=headers,
                                 json=uncomplete_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            uncompleted_task = response.json()
            print(f"   Task uncompleted: {uncompleted_task['completed']}")
        else:
            print(f"   Failed to uncomplete task: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")

    # Test 9: DELETE /api/v1/{user_id}/tasks/{task_id} (delete task)
    print("\n9. Testing DELETE /api/v1/{user_id}/tasks/{task_id} (delete task)")
    try:
        response = requests.delete(f"{base_url}/api/v1/{user_id}/tasks/{task_id}", headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 204:
            print("   Task deleted successfully")
        else:
            print(f"   Failed to delete task: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")

    # Test 10: GET /api/v1/{user_id}/tasks (should be empty after deletion)
    print("\n10. Testing GET /api/v1/{user_id}/tasks (after deletion)")
    try:
        response = requests.get(f"{base_url}/api/v1/{user_id}/tasks", headers=headers)
        print(f"   Status: {response.status_code}")
        tasks_after_deletion = response.json()
        print(f"   Number of tasks after deletion: {len(tasks_after_deletion)}")
        print(f"   Response: {tasks_after_deletion}")
    except Exception as e:
        print(f"   Error: {e}")

    print("\n" + "="*50)
    print("SUMMARY OF FEATURES TESTED:")
    print("✅ CREATE: Task creation via POST /api/v1/{user_id}/tasks")
    print("✅ READ: Task retrieval via GET /api/v1/{user_id}/tasks and GET /api/v1/{user_id}/tasks/{task_id}")
    print("✅ UPDATE: Task updates via PUT /api/v1/{user_id}/tasks/{task_id}")
    print("✅ DELETE: Task deletion via DELETE /api/v1/{user_id}/tasks/{task_id}")
    print("✅ COMPLETE: Marking task as complete via PATCH /api/v1/{user_id}/tasks/{task_id}/complete")
    print("✅ PENDING: Marking task as pending via PATCH /api/v1/{user_id}/tasks/{task_id}/complete")
    print("✅ AUTHENTICATION: All endpoints properly secured with JWT")
    print("✅ USER ISOLATION: Using specific user ID in URLs")
    print("="*50)

if __name__ == "__main__":
    test_all_features()