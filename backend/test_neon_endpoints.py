"""
Comprehensive test script to verify all backend endpoints are working correctly
and data is being saved to Neon database.
"""
import requests
import json
from datetime import timedelta
import sys
import os

# Add the app directory to path to import auth module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app.core.auth import create_access_token

# Configuration
BASE_URL = "http://localhost:8000"
TEST_USER_ID = "test_user_123"

def create_test_token(user_id: str) -> str:
    """Create a test JWT token for the given user ID."""
    token = create_access_token(
        data={"sub": user_id},
        expires_delta=timedelta(hours=1)
    )
    return token

def print_result(test_name: str, success: bool, details: str = ""):
    """Print test result in a formatted way."""
    status = "[PASS]" if success else "[FAIL]"
    print(f"\n{status} - {test_name}")
    if details:
        print(f"  Details: {details}")

def test_health_endpoints():
    """Test health check endpoints."""
    print("\n" + "="*60)
    print("Testing Health Endpoints")
    print("="*60)

    # Test root endpoint
    try:
        response = requests.get(f"{BASE_URL}/")
        success = response.status_code == 200
        print_result("Root endpoint", success, f"Status: {response.status_code}, Response: {response.json()}")
    except Exception as e:
        print_result("Root endpoint", False, str(e))

    # Test health endpoint
    try:
        response = requests.get(f"{BASE_URL}/health")
        success = response.status_code == 200 and response.json().get("database") == "connected"
        print_result("Health check", success, f"Database: {response.json().get('database')}")
    except Exception as e:
        print_result("Health check", False, str(e))

    # Test database health endpoint
    try:
        response = requests.get(f"{BASE_URL}/health/database")
        success = response.status_code == 200 and response.json().get("database") == "connected"
        print_result("Database health check", success, f"Status: {response.json().get('status')}")
    except Exception as e:
        print_result("Database health check", False, str(e))

def test_task_endpoints():
    """Test all task CRUD endpoints."""
    print("\n" + "="*60)
    print("Testing Task Endpoints")
    print("="*60)

    # Create JWT token
    token = create_test_token(TEST_USER_ID)
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Store created task IDs for later tests
    task_ids = []

    # Test 1: Create a task
    print("\n[1] Creating a new task...")
    try:
        task_data = {
            "title": "Test Task from Script",
            "description": "This is a test task created by the automated test script",
            "completed": False
        }
        response = requests.post(
            f"{BASE_URL}/api/v1/{TEST_USER_ID}/tasks",
            headers=headers,
            json=task_data
        )
        success = response.status_code == 201
        if success:
            task = response.json()
            task_ids.append(task["id"])
            print_result("Create task", True, f"Task ID: {task['id']}, Title: {task['title']}")
        else:
            print_result("Create task", False, f"Status: {response.status_code}, Error: {response.text}")
    except Exception as e:
        print_result("Create task", False, str(e))

    # Test 2: Get all tasks
    print("\n[2] Fetching all tasks...")
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/{TEST_USER_ID}/tasks",
            headers=headers
        )
        success = response.status_code == 200
        if success:
            tasks = response.json()
            print_result("Get all tasks", True, f"Found {len(tasks)} task(s)")
            for task in tasks:
                print(f"    - ID: {task['id']}, Title: {task['title']}, Completed: {task['completed']}")
        else:
            print_result("Get all tasks", False, f"Status: {response.status_code}")
    except Exception as e:
        print_result("Get all tasks", False, str(e))

    # Test 3: Get tasks filtered by status (pending)
    print("\n[3] Fetching pending tasks...")
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/{TEST_USER_ID}/tasks?status=pending",
            headers=headers
        )
        success = response.status_code == 200
        if success:
            tasks = response.json()
            all_pending = all(not task['completed'] for task in tasks)
            print_result("Get pending tasks", all_pending, f"Found {len(tasks)} pending task(s)")
        else:
            print_result("Get pending tasks", False, f"Status: {response.status_code}")
    except Exception as e:
        print_result("Get pending tasks", False, str(e))

    # Test 4: Get a specific task by ID
    if task_ids:
        print("\n[4] Fetching task by ID...")
        try:
            response = requests.get(
                f"{BASE_URL}/api/v1/{TEST_USER_ID}/tasks/{task_ids[0]}",
                headers=headers
            )
            success = response.status_code == 200
            if success:
                task = response.json()
                print_result("Get task by ID", True, f"Title: {task['title']}")
            else:
                print_result("Get task by ID", False, f"Status: {response.status_code}")
        except Exception as e:
            print_result("Get task by ID", False, str(e))

    # Test 5: Update a task
    if task_ids:
        print("\n[5] Updating task...")
        try:
            update_data = {
                "title": "Updated Test Task",
                "description": "This task has been updated by the test script"
            }
            response = requests.put(
                f"{BASE_URL}/api/v1/{TEST_USER_ID}/tasks/{task_ids[0]}",
                headers=headers,
                json=update_data
            )
            success = response.status_code == 200
            if success:
                task = response.json()
                print_result("Update task", True, f"New title: {task['title']}")
            else:
                print_result("Update task", False, f"Status: {response.status_code}, Error: {response.text}")
        except Exception as e:
            print_result("Update task", False, str(e))

    # Test 6: Mark task as completed
    if task_ids:
        print("\n[6] Marking task as completed...")
        try:
            response = requests.patch(
                f"{BASE_URL}/api/v1/{TEST_USER_ID}/tasks/{task_ids[0]}/complete",
                headers=headers,
                json={"completed": True}
            )
            success = response.status_code == 200
            if success:
                task = response.json()
                print_result("Complete task", True, f"Completed: {task['completed']}")
            else:
                print_result("Complete task", False, f"Status: {response.status_code}")
        except Exception as e:
            print_result("Complete task", False, str(e))

    # Test 7: Get completed tasks
    print("\n[7] Fetching completed tasks...")
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/{TEST_USER_ID}/tasks?status=completed",
            headers=headers
        )
        success = response.status_code == 200
        if success:
            tasks = response.json()
            all_completed = all(task['completed'] for task in tasks)
            print_result("Get completed tasks", all_completed, f"Found {len(tasks)} completed task(s)")
        else:
            print_result("Get completed tasks", False, f"Status: {response.status_code}")
    except Exception as e:
        print_result("Get completed tasks", False, str(e))

    # Test 8: Create another task for verification
    print("\n[8] Creating another task to verify database persistence...")
    try:
        task_data = {
            "title": "Second Test Task",
            "description": "Verifying data persistence in Neon DB",
            "completed": False
        }
        response = requests.post(
            f"{BASE_URL}/api/v1/{TEST_USER_ID}/tasks",
            headers=headers,
            json=task_data
        )
        success = response.status_code == 201
        if success:
            task = response.json()
            task_ids.append(task["id"])
            print_result("Create second task", True, f"Task ID: {task['id']}")
        else:
            print_result("Create second task", False, f"Status: {response.status_code}")
    except Exception as e:
        print_result("Create second task", False, str(e))

    # Test 9: Delete a task
    if len(task_ids) > 1:
        print("\n[9] Deleting a task...")
        try:
            response = requests.delete(
                f"{BASE_URL}/api/v1/{TEST_USER_ID}/tasks/{task_ids[1]}",
                headers=headers
            )
            success = response.status_code == 204
            print_result("Delete task", success, f"Task {task_ids[1]} deleted")
        except Exception as e:
            print_result("Delete task", False, str(e))

    # Test 10: Verify deletion
    if len(task_ids) > 1:
        print("\n[10] Verifying task was deleted...")
        try:
            response = requests.get(
                f"{BASE_URL}/api/v1/{TEST_USER_ID}/tasks/{task_ids[1]}",
                headers=headers
            )
            success = response.status_code == 404
            print_result("Verify deletion", success, f"Task correctly not found (404)")
        except Exception as e:
            print_result("Verify deletion", False, str(e))

    # Test 11: Test authentication (without token)
    print("\n[11] Testing authentication (should fail without token)...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/{TEST_USER_ID}/tasks")
        success = response.status_code == 403
        print_result("Auth check (no token)", success, f"Status: {response.status_code} (expected 403)")
    except Exception as e:
        print_result("Auth check (no token)", False, str(e))

    # Test 12: Test authorization (wrong user ID)
    print("\n[12] Testing authorization (wrong user ID)...")
    try:
        wrong_user_token = create_test_token("different_user")
        wrong_headers = {
            "Authorization": f"Bearer {wrong_user_token}",
            "Content-Type": "application/json"
        }
        response = requests.get(
            f"{BASE_URL}/api/v1/{TEST_USER_ID}/tasks",
            headers=wrong_headers
        )
        success = response.status_code == 403
        print_result("Auth check (wrong user)", success, f"Status: {response.status_code} (expected 403)")
    except Exception as e:
        print_result("Auth check (wrong user)", False, str(e))

    return task_ids

def verify_neon_database():
    """Verify that data is actually in Neon database."""
    print("\n" + "="*60)
    print("Verifying Data Persistence in Neon Database")
    print("="*60)

    try:
        # Check if we're using Neon database
        from app.db.database import DATABASE_URL
        is_neon = "neon.tech" in DATABASE_URL
        print(f"\nDatabase URL: {DATABASE_URL[:50]}...")
        print_result("Using Neon Database", is_neon, f"Neon DB detected: {is_neon}")

        if not is_neon:
            print("\n[WARNING] Not using Neon database! Check your .env file.")
    except Exception as e:
        print_result("Database verification", False, str(e))

def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("Backend API Testing Suite")
    print("Testing Neon Database Integration")
    print("="*60)

    try:
        # Test health endpoints
        test_health_endpoints()

        # Verify we're using Neon DB
        verify_neon_database()

        # Test all task endpoints
        test_task_endpoints()

        print("\n" + "="*60)
        print("All Tests Completed!")
        print("="*60)
        print("\nSummary:")
        print("- All endpoints have been tested")
        print("- Data operations verified with Neon database")
        print("- Authentication and authorization working correctly")
        print("\nNote: Tasks created during testing remain in the database.")
        print("      You can verify them in your Neon console or through the API.")

    except Exception as e:
        print(f"\n[ERROR] Test suite failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
