import pytest
from sqlmodel import Session
from app.crud.task import create_task, get_tasks, get_task_by_id, update_task, delete_task, update_task_completion
from app.models.task import TaskCreate, TaskUpdate, TaskComplete
from uuid import UUID


def test_create_task_success(db_session: Session, valid_user_id: str, sample_task_data: dict):
    """
    Test successful task creation.
    """
    task_in = TaskCreate(**sample_task_data)
    created_task = create_task(session=db_session, task_in=task_in, user_id=valid_user_id)

    assert created_task.title == sample_task_data["title"]
    assert created_task.description == sample_task_data["description"]
    assert created_task.user_id == valid_user_id
    assert created_task.completed is False
    assert created_task.id is not None


def test_get_tasks_empty(db_session: Session, valid_user_id: str):
    """
    Test getting tasks when none exist for user.
    """
    tasks = get_tasks(session=db_session, user_id=valid_user_id)
    assert len(tasks) == 0


def test_get_tasks_with_data(db_session: Session, valid_user_id: str, sample_task_data: dict):
    """
    Test getting tasks when some exist for user.
    """
    # Create a task first
    task_in = TaskCreate(**sample_task_data)
    create_task(session=db_session, task_in=task_in, user_id=valid_user_id)

    # Get tasks for user
    tasks = get_tasks(session=db_session, user_id=valid_user_id)
    assert len(tasks) == 1
    assert tasks[0].title == sample_task_data["title"]


def test_get_tasks_different_users(db_session: Session, valid_user_id: str, sample_task_data: dict):
    """
    Test that users only get their own tasks.
    """
    # Create task for first user
    task_in = TaskCreate(**sample_task_data)
    create_task(session=db_session, task_in=task_in, user_id=valid_user_id)

    # Create task for second user
    user2_id = "test-user-456"
    create_task(session=db_session, task_in=task_in, user_id=user2_id)

    # Each user should only see their own task
    user1_tasks = get_tasks(session=db_session, user_id=valid_user_id)
    user2_tasks = get_tasks(session=db_session, user_id=user2_id)

    assert len(user1_tasks) == 1
    assert len(user2_tasks) == 1
    assert user1_tasks[0].user_id == valid_user_id
    assert user2_tasks[0].user_id == user2_id


def test_get_task_by_id_found(db_session: Session, valid_user_id: str, sample_task_data: dict):
    """
    Test getting a specific task by ID when it exists.
    """
    # Create task
    task_in = TaskCreate(**sample_task_data)
    created_task = create_task(session=db_session, task_in=task_in, user_id=valid_user_id)

    # Get by ID
    retrieved_task = get_task_by_id(session=db_session, task_id=created_task.id, user_id=valid_user_id)

    assert retrieved_task is not None
    assert retrieved_task.id == created_task.id
    assert retrieved_task.title == sample_task_data["title"]


def test_get_task_by_id_not_found(db_session: Session, valid_user_id: str):
    """
    Test getting a specific task by ID when it doesn't exist.
    """
    fake_task_id = UUID("12345678-1234-5678-1234-567812345678")

    retrieved_task = get_task_by_id(session=db_session, task_id=fake_task_id, user_id=valid_user_id)

    assert retrieved_task is None


def test_get_task_by_id_wrong_user(db_session: Session, valid_user_id: str, sample_task_data: dict):
    """
    Test getting a specific task by ID when it belongs to a different user.
    """
    # Create task for first user
    task_in = TaskCreate(**sample_task_data)
    created_task = create_task(session=db_session, task_in=task_in, user_id=valid_user_id)

    # Try to get it as a different user
    different_user = "different-user-123"
    retrieved_task = get_task_by_id(session=db_session, task_id=created_task.id, user_id=different_user)

    assert retrieved_task is None


def test_update_task_success(db_session: Session, valid_user_id: str, sample_task_data: dict):
    """
    Test successful task update.
    """
    # Create task
    task_in = TaskCreate(**sample_task_data)
    created_task = create_task(session=db_session, task_in=task_in, user_id=valid_user_id)

    # Update task
    update_data = TaskUpdate(title="Updated Title", description="Updated Description")
    updated_task = update_task(session=db_session, task_id=created_task.id, user_id=valid_user_id, task_in=update_data)

    assert updated_task is not None
    assert updated_task.title == "Updated Title"
    assert updated_task.description == "Updated Description"


def test_update_task_not_found(db_session: Session, valid_user_id: str):
    """
    Test updating a task that doesn't exist.
    """
    fake_task_id = UUID("12345678-1234-5678-1234-567812345678")
    update_data = TaskUpdate(title="Updated Title")

    updated_task = update_task(session=db_session, task_id=fake_task_id, user_id=valid_user_id, task_in=update_data)

    assert updated_task is None


def test_delete_task_success(db_session: Session, valid_user_id: str, sample_task_data: dict):
    """
    Test successful task deletion.
    """
    # Create task
    task_in = TaskCreate(**sample_task_data)
    created_task = create_task(session=db_session, task_in=task_in, user_id=valid_user_id)

    # Verify it exists
    retrieved_task = get_task_by_id(session=db_session, task_id=created_task.id, user_id=valid_user_id)
    assert retrieved_task is not None

    # Delete task
    success = delete_task(session=db_session, task_id=created_task.id, user_id=valid_user_id)
    assert success is True

    # Verify it's gone
    retrieved_task = get_task_by_id(session=db_session, task_id=created_task.id, user_id=valid_user_id)
    assert retrieved_task is None


def test_delete_task_not_found(db_session: Session, valid_user_id: str):
    """
    Test deleting a task that doesn't exist.
    """
    fake_task_id = UUID("12345678-1234-5678-1234-567812345678")

    success = delete_task(session=db_session, task_id=fake_task_id, user_id=valid_user_id)

    assert success is False


def test_update_task_completion_success(db_session: Session, valid_user_id: str, sample_task_data: dict):
    """
    Test successful task completion status update.
    """
    # Create task
    task_in = TaskCreate(**sample_task_data)
    created_task = create_task(session=db_session, task_in=task_in, user_id=valid_user_id)

    # Verify it's initially not completed
    assert created_task.completed is False

    # Update completion status
    completion_data = TaskComplete(completed=True)
    updated_task = update_task_completion(session=db_session, task_id=created_task.id, user_id=valid_user_id, task_complete=completion_data)

    assert updated_task is not None
    assert updated_task.completed is True

    # Change back to not completed
    completion_data = TaskComplete(completed=False)
    updated_task = update_task_completion(session=db_session, task_id=created_task.id, user_id=valid_user_id, task_complete=completion_data)

    assert updated_task is not None
    assert updated_task.completed is False