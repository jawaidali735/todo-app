import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.pool import StaticPool
from app.main import app
from app.db.database import get_session
from app.models.task import Task
from unittest.mock import patch
import os
import uuid

# Use an in-memory SQLite database for testing
TEST_DATABASE_URL = "sqlite:///./test.db"

# Create test engine
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

def get_test_session():
    """
    Get a test database session.
    """
    with Session(engine) as session:
        yield session

@pytest.fixture(scope="function")
def db_session():
    """
    Create a test database session with tables created.
    """
    # Create all tables
    SQLModel.metadata.create_all(bind=engine)

    with Session(engine) as session:
        yield session

    # Cleanup - drop all tables after test
    SQLModel.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    """
    Create a test client with dependency overrides.
    """
    # Override the get_session dependency
    app.dependency_overrides[get_session] = lambda: db_session

    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
def mock_jwt_secret():
    """
    Mock the JWT secret for testing.
    """
    with patch("app.core.config.settings.BETTER_AUTH_SECRET", "test-secret-key"):
        yield "test-secret-key"

@pytest.fixture
def valid_user_id():
    """
    Provide a valid user ID for testing.
    """
    return "test-user-123"

@pytest.fixture
def sample_task_data():
    """
    Provide sample task data for testing.
    """
    return {
        "title": "Test Task",
        "description": "This is a test task description"
    }

@pytest.fixture
def expired_token():
    """
    Provide an expired JWT token for testing.
    """
    import time
    import jwt
    from datetime import datetime, timedelta

    payload = {
        "sub": "test-user-123",
        "exp": datetime.utcnow() - timedelta(seconds=1),  # Expired 1 second ago
        "iat": datetime.utcnow() - timedelta(hours=1)
    }
    token = jwt.encode(payload, "test-secret-key", algorithm="HS256")
    return token

@pytest.fixture
def valid_token():
    """
    Provide a valid JWT token for testing.
    """
    import time
    import jwt
    from datetime import datetime, timedelta

    payload = {
        "sub": "test-user-123",
        "exp": datetime.utcnow() + timedelta(hours=1),  # Expires in 1 hour
        "iat": datetime.utcnow()
    }
    token = jwt.encode(payload, "test-secret-key", algorithm="HS256")
    return token