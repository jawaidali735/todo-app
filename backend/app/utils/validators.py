from typing import Optional
from app.models.task import TaskCreate, TaskUpdate
import re

def validate_task_title(title: str) -> bool:
    """
    Validates that a task title is not empty and meets length requirements.

    Args:
        title: The task title to validate

    Returns:
        True if valid, False otherwise
    """
    if not title or not title.strip():
        return False

    # Check length (max 200 characters as per requirements)
    if len(title) > 200:
        return False

    return True


def validate_task_description(description: Optional[str]) -> bool:
    """
    Validates that a task description meets length requirements if provided.

    Args:
        description: The task description to validate (can be None)

    Returns:
        True if valid, False otherwise
    """
    if description is None:
        return True

    # Check length (max 1000 characters)
    if len(description) > 1000:
        return False

    return True


def validate_task_completion_status(completed: bool) -> bool:
    """
    Validates that the completion status is a boolean value.

    Args:
        completed: The completion status to validate

    Returns:
        True if valid, False otherwise
    """
    return isinstance(completed, bool)


def validate_user_id(user_id: str) -> bool:
    """
    Validates that a user ID is not empty and meets basic requirements.

    Args:
        user_id: The user ID to validate

    Returns:
        True if valid, False otherwise
    """
    if not user_id or not user_id.strip():
        return False

    # Basic check for reasonable length
    if len(user_id) > 100:
        return False

    return True


def validate_task_data(task_data: TaskCreate) -> tuple[bool, Optional[str]]:
    """
    Validates task creation data.

    Args:
        task_data: The task data to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not validate_task_title(task_data.title):
        return False, "Task title is required and must be 1-200 characters"

    if not validate_task_description(task_data.description):
        return False, "Task description exceeds maximum length of 1000 characters"

    return True, None


def validate_task_update_data(task_data: TaskUpdate) -> tuple[bool, Optional[str]]:
    """
    Validates task update data.

    Args:
        task_data: The task update data to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if task_data.title is not None and not validate_task_title(task_data.title):
        return False, "Task title must be 1-200 characters if provided"

    if task_data.description is not None and not validate_task_description(task_data.description):
        return False, "Task description exceeds maximum length of 1000 characters"

    return True, None