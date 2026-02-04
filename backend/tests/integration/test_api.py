import pytest
from fastapi.testclient import TestClient
from app.models.task import Task
from uuid import UUID
import json


def test_create_task_success(client: TestClient, valid_user_id: str, valid_token: str, sample_task_data: dict):
    """
    Test successful task creation via API.
    """
    response = client.post(
        f"/api/v1/{valid_user_id}/tasks",
        json=sample_task_data,
        headers={"Authorization": f"Bearer {valid_token}"}
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == sample_task_data["title"]
    assert data["description"] == sample_task_data["description"]
    assert data["user_id"] == valid_user_id
    assert data["completed"] is False
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_create_task_invalid_token(client: TestClient, valid_user_id: str, sample_task_data: dict):
    """
    Test task creation with invalid token returns 401.
    """
    response = client.post(
        f"/api/v1/{valid_user_id}/tasks",
        json=sample_task_data,
        headers={"Authorization": "Bearer invalid-token"}
    )

    assert response.status_code == 401


def test_create_task_user_id_mismatch(client: TestClient, valid_user_id: str, valid_token: str, sample_task_data: dict):
    """
    Test task creation with token user ID != URL user ID returns 403.
    """
    different_user_id = "different-user-123"
    response = client.post(
        f"/api/v1/{different_user_id}/tasks",
        json=sample_task_data,
        headers={"Authorization": f"Bearer {valid_token}"}
    )

    assert response.status_code == 403


def test_list_tasks_empty(client: TestClient, valid_user_id: str, valid_token: str):
    """
    Test listing tasks when none exist returns empty list.
    """
    response = client.get(
        f"/api/v1/{valid_user_id}/tasks",
        headers={"Authorization": f"Bearer {valid_token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data == []


def test_list_tasks_with_data(client: TestClient, valid_user_id: str, valid_token: str, sample_task_data: dict):
    """
    Test listing tasks when some exist returns correct data.
    """
    # Create a task first
    create_response = client.post(
        f"/api/v1/{valid_user_id}/tasks",
        json=sample_task_data,
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert create_response.status_code == 201
    created_task = create_response.json()

    # List tasks
    response = client.get(
        f"/api/v1/{valid_user_id}/tasks",
        headers={"Authorization": f"Bearer {valid_token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == created_task["id"]
    assert data[0]["title"] == sample_task_data["title"]


def test_get_single_task_success(client: TestClient, valid_user_id: str, valid_token: str, sample_task_data: dict):
    """
    Test getting a single task by ID.
    """
    # Create a task first
    create_response = client.post(
        f"/api/v1/{valid_user_id}/tasks",
        json=sample_task_data,
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert create_response.status_code == 201
    created_task = create_response.json()

    # Get the task
    response = client.get(
        f"/api/v1/{valid_user_id}/tasks/{created_task['id']}",
        headers={"Authorization": f"Bearer {valid_token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created_task["id"]
    assert data["title"] == sample_task_data["title"]


def test_get_single_task_not_found(client: TestClient, valid_user_id: str, valid_token: str):
    """
    Test getting a non-existent task returns 404.
    """
    fake_task_id = "12345678-1234-5678-1234-567812345678"

    response = client.get(
        f"/api/v1/{valid_user_id}/tasks/{fake_task_id}",
        headers={"Authorization": f"Bearer {valid_token}"}
    )

    assert response.status_code == 404


def test_update_task_success(client: TestClient, valid_user_id: str, valid_token: str, sample_task_data: dict):
    """
    Test updating a task successfully.
    """
    # Create a task first
    create_response = client.post(
        f"/api/v1/{valid_user_id}/tasks",
        json=sample_task_data,
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert create_response.status_code == 201
    created_task = create_response.json()

    # Update the task
    update_data = {"title": "Updated Title", "description": "Updated Description"}
    response = client.put(
        f"/api/v1/{valid_user_id}/tasks/{created_task['id']}",
        json=update_data,
        headers={"Authorization": f"Bearer {valid_token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created_task["id"]
    assert data["title"] == "Updated Title"
    assert data["description"] == "Updated Description"


def test_update_task_not_found(client: TestClient, valid_user_id: str, valid_token: str):
    """
    Test updating a non-existent task returns 404.
    """
    fake_task_id = "12345678-1234-5678-1234-567812345678"
    update_data = {"title": "Updated Title"}

    response = client.put(
        f"/api/v1/{valid_user_id}/tasks/{fake_task_id}",
        json=update_data,
        headers={"Authorization": f"Bearer {valid_token}"}
    )

    assert response.status_code == 404


def test_delete_task_success(client: TestClient, valid_user_id: str, valid_token: str, sample_task_data: dict):
    """
    Test deleting a task successfully.
    """
    # Create a task first
    create_response = client.post(
        f"/api/v1/{valid_user_id}/tasks",
        json=sample_task_data,
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert create_response.status_code == 201
    created_task = create_response.json()

    # Delete the task
    response = client.delete(
        f"/api/v1/{valid_user_id}/tasks/{created_task['id']}",
        headers={"Authorization": f"Bearer {valid_token}"}
    )

    assert response.status_code == 204

    # Verify it's gone
    get_response = client.get(
        f"/api/v1/{valid_user_id}/tasks/{created_task['id']}",
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert get_response.status_code == 404


def test_delete_task_not_found(client: TestClient, valid_user_id: str, valid_token: str):
    """
    Test deleting a non-existent task returns 404.
    """
    fake_task_id = "12345678-1234-5678-1234-567812345678"

    response = client.delete(
        f"/api/v1/{valid_user_id}/tasks/{fake_task_id}",
        headers={"Authorization": f"Bearer {valid_token}"}
    )

    assert response.status_code == 404


def test_update_task_completion_success(client: TestClient, valid_user_id: str, valid_token: str, sample_task_data: dict):
    """
    Test updating task completion status successfully.
    """
    # Create a task first
    create_response = client.post(
        f"/api/v1/{valid_user_id}/tasks",
        json=sample_task_data,
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert create_response.status_code == 201
    created_task = create_response.json()

    # Verify it's initially not completed
    assert created_task["completed"] is False

    # Update completion status
    completion_data = {"completed": True}
    response = client.patch(
        f"/api/v1/{valid_user_id}/tasks/{created_task['id']}/complete",
        json=completion_data,
        headers={"Authorization": f"Bearer {valid_token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created_task["id"]
    assert data["completed"] is True

    # Change back to not completed
    completion_data = {"completed": False}
    response = client.patch(
        f"/api/v1/{valid_user_id}/tasks/{created_task['id']}/complete",
        json=completion_data,
        headers={"Authorization": f"Bearer {valid_token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created_task["id"]
    assert data["completed"] is False


def test_filter_tasks_by_status(client: TestClient, valid_user_id: str, valid_token: str, sample_task_data: dict):
    """
    Test filtering tasks by status (completed/pending).
    """
    # Create a completed task
    create_response = client.post(
        f"/api/v1/{valid_user_id}/tasks",
        json=sample_task_data,
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert create_response.status_code == 201
    created_task = create_response.json()

    # Complete the task
    completion_response = client.patch(
        f"/api/v1/{valid_user_id}/tasks/{created_task['id']}/complete",
        json={"completed": True},
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert completion_response.status_code == 200

    # Create a pending task
    pending_task_data = {**sample_task_data, "title": "Pending Task"}
    pending_response = client.post(
        f"/api/v1/{valid_user_id}/tasks",
        json=pending_task_data,
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert pending_response.status_code == 201

    # Get completed tasks only
    completed_response = client.get(
        f"/api/v1/{valid_user_id}/tasks?status=completed",
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert completed_response.status_code == 200
    completed_tasks = completed_response.json()
    assert len(completed_tasks) == 1
    assert completed_tasks[0]["id"] == created_task["id"]
    assert completed_tasks[0]["completed"] is True

    # Get pending tasks only
    pending_response = client.get(
        f"/api/v1/{valid_user_id}/tasks?status=pending",
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert pending_response.status_code == 200
    pending_tasks = pending_response.json()
    assert len(pending_tasks) == 1
    assert pending_tasks[0]["title"] == "Pending Task"
    assert pending_tasks[0]["completed"] is False

    # Get all tasks
    all_response = client.get(
        f"/api/v1/{valid_user_id}/tasks?status=all",
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert all_response.status_code == 200
    all_tasks = all_response.json()
    assert len(all_tasks) == 2


def test_health_endpoint(client: TestClient):
    """
    Test the health endpoint returns healthy status.
    """
    response = client.get("/health")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"


def test_database_health_endpoint(client: TestClient):
    """
    Test the database health endpoint returns healthy status.
    """
    response = client.get("/health/database")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"