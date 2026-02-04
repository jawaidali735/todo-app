from fastapi import HTTPException, status
from typing import Optional


class TaskNotFoundException(HTTPException):
    def __init__(self, task_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )


class UserMismatchException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: user ID in token does not match user ID in URL"
        )


class ValidationErrorException(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )


class DatabaseConnectionException(HTTPException):
    def __init__(self, message: Optional[str] = None):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=message or "Database connection unavailable"
        )


class UnauthorizedAccessException(HTTPException):
    def __init__(self, message: Optional[str] = None):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=message or "Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def create_error_response(status_code: int, message: str, error_code: Optional[str] = None):
    """
    Create a standardized error response.

    Args:
        status_code: HTTP status code
        message: Error message
        error_code: Optional application-specific error code

    Returns:
        Dictionary with standardized error response format
    """
    error_response = {
        "status_code": status_code,
        "message": message,
        "timestamp": __import__('datetime').datetime.utcnow().isoformat()
    }

    if error_code:
        error_response["error_code"] = error_code

    return error_response