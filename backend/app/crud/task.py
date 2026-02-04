from sqlmodel import Session, select, update
from typing import List, Optional
from app.models.task import Task, TaskCreate, TaskUpdate, TaskComplete
from app.utils.validators import validate_task_data, validate_task_update_data
from uuid import UUID
from datetime import datetime, UTC

def create_task(*, session: Session, task_in: TaskCreate, user_id: str) -> Task:
    """
    Create a new task for a specific user.

    Args:
        session: Database session
        task_in: Task creation data
        user_id: ID of the user creating the task

    Returns:
        Created Task object

    Raises:
        ValueError: If validation fails
    """
    # Validate input data
    is_valid, error_msg = validate_task_data(task_in)
    if not is_valid:
        raise ValueError(error_msg)

    # Create task object
    task_data = task_in.model_dump()
    task = Task(**task_data, user_id=user_id)

    # Add to session and commit
    session.add(task)
    session.commit()
    session.refresh(task)

    return task


def get_tasks(*, session: Session, user_id: str, completed: Optional[bool] = None) -> List[Task]:
    """
    Get all tasks for a specific user, with optional filtering by completion status.

    Args:
        session: Database session
        user_id: ID of the user whose tasks to retrieve
        completed: Optional filter for completion status (None=all, True=completed, False=pending)

    Returns:
        List of Task objects
    """
    query = select(Task).where(Task.user_id == user_id)

    if completed is not None:
        query = query.where(Task.completed == completed)

    tasks = session.exec(query).all()
    return tasks


def get_task_by_id(*, session: Session, task_id: UUID, user_id: str) -> Optional[Task]:
    """
    Get a specific task by ID for a specific user.

    Args:
        session: Database session
        task_id: ID of the task to retrieve
        user_id: ID of the user who owns the task

    Returns:
        Task object if found and owned by user, None otherwise
    """
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()
    return task


def update_task(*, session: Session, task_id: UUID, user_id: str, task_in: TaskUpdate) -> Optional[Task]:
    """
    Update a specific task for a specific user.

    Args:
        session: Database session
        task_id: ID of the task to update
        user_id: ID of the user who owns the task
        task_in: Task update data

    Returns:
        Updated Task object if successful, None if task not found

    Raises:
        ValueError: If validation fails
    """
    # Validate input data
    is_valid, error_msg = validate_task_update_data(task_in)
    if not is_valid:
        raise ValueError(error_msg)

    # Get the existing task
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()

    if not task:
        return None

    # Prepare update data
    update_data = task_in.model_dump(exclude_unset=True)

    # Update the task
    for field, value in update_data.items():
        setattr(task, field, value)

    # Update timestamp
    task.updated_at = datetime.now(UTC)

    # Commit changes
    session.add(task)
    session.commit()
    session.refresh(task)

    return task


def update_task_completion(*, session: Session, task_id: UUID, user_id: str, task_complete: TaskComplete) -> Optional[Task]:
    """
    Update the completion status of a specific task for a specific user.

    Args:
        session: Database session
        task_id: ID of the task to update
        user_id: ID of the user who owns the task
        task_complete: Task completion data

    Returns:
        Updated Task object if successful, None if task not found
    """
    # Get the existing task
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()

    if not task:
        return None

    # Update completion status
    task.completed = task_complete.completed

    # Update timestamp
    task.updated_at = datetime.now(UTC)

    # Commit changes
    session.add(task)
    session.commit()
    session.refresh(task)

    return task


def delete_task(*, session: Session, task_id: UUID, user_id: str) -> bool:
    """
    Delete a specific task for a specific user.

    Args:
        session: Database session
        task_id: ID of the task to delete
        user_id: ID of the user who owns the task

    Returns:
        True if deletion was successful, False if task not found
    """
    # Get the existing task
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()

    if not task:
        return False

    # Delete the task
    session.delete(task)
    session.commit()

    return True