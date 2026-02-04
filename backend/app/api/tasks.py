from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from sqlmodel import Session
from uuid import UUID

from app.db.database import get_session
from app.core.auth import get_current_user
from app.models.task import TaskRead, TaskCreate, TaskUpdate, TaskComplete
from app.crud.task import (
    create_task,
    get_tasks,
    get_task_by_id,
    update_task,
    update_task_completion,
    delete_task
)

router = APIRouter(prefix="/api/v1/{user_id}", tags=["tasks"])

@router.get("/tasks", response_model=List[TaskRead])
async def list_tasks(
    user_id: str,
    status: Optional[str] = Query(None, description="Filter tasks by status: all, pending, completed", pattern=r"^(all|pending|completed)$"),
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get all tasks for the authenticated user, with optional filtering by completion status.
    """
    # Verify that the user in the token matches the user in the URL
    if current_user != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: user ID in token does not match user ID in URL"
        )

    # Convert status parameter to boolean for the database query
    completed_filter = None
    if status == "completed":
        completed_filter = True
    elif status == "pending":
        completed_filter = False
    # If status is "all" or None, we don't filter by completion status

    tasks = get_tasks(session=session, user_id=user_id, completed=completed_filter)
    return tasks


@router.post("/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_new_task(
    user_id: str,
    task_in: TaskCreate,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the authenticated user.
    """
    # Verify that the user in the token matches the user in the URL
    if current_user != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: user ID in token does not match user ID in URL"
        )

    try:
        task = create_task(session=session, task_in=task_in, user_id=user_id)
        return task
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/tasks/{task_id}", response_model=TaskRead)
async def get_task(
    user_id: str,
    task_id: UUID,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get a specific task by ID for the authenticated user.
    """
    # Verify that the user in the token matches the user in the URL
    if current_user != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: user ID in token does not match user ID in URL"
        )

    task = get_task_by_id(session=session, task_id=task_id, user_id=user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


@router.put("/tasks/{task_id}", response_model=TaskRead)
async def update_existing_task(
    user_id: str,
    task_id: UUID,
    task_in: TaskUpdate,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update a specific task for the authenticated user.
    """
    # Verify that the user in the token matches the user in the URL
    if current_user != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: user ID in token does not match user ID in URL"
        )

    task = update_task(session=session, task_id=task_id, user_id=user_id, task_in=task_in)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


@router.patch("/tasks/{task_id}/complete", response_model=TaskRead)
async def update_task_completion_status(
    user_id: str,
    task_id: UUID,
    task_complete: TaskComplete,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update the completion status of a specific task for the authenticated user.
    """
    # Verify that the user in the token matches the user in the URL
    if current_user != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: user ID in token does not match user ID in URL"
        )

    task = update_task_completion(session=session, task_id=task_id, user_id=user_id, task_complete=task_complete)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_task(
    user_id: str,
    task_id: UUID,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a specific task for the authenticated user.
    """
    # Verify that the user in the token matches the user in the URL
    if current_user != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: user ID in token does not match user ID in URL"
        )

    success = delete_task(session=session, task_id=task_id, user_id=user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return


@router.get("/", include_in_schema=False)
async def root_redirect():
    """
    Root endpoint for the user-specific API - redirects to task listing.
    """
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Endpoint not found. Try /api/v1/{user_id}/tasks"
    )