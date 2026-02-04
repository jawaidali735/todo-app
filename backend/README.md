# Todo Backend API

A FastAPI-based backend service for the todo application with JWT authentication and PostgreSQL persistence.

## Features

- JWT-based authentication and authorization
- RESTful API endpoints for task management
- User isolation - each user can only access their own tasks
- PostgreSQL database with proper indexing
- Comprehensive error handling
- Health check endpoints
- Performance monitoring

## Prerequisites

- Python 3.11+
- PostgreSQL database (Neon Serverless recommended)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd todo-app/backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and set the required values:
   - `DATABASE_URL`: PostgreSQL connection string
   - `BETTER_AUTH_SECRET`: Secret key for JWT verification (must match frontend)
   - `JWT_ALGORITHM`: Algorithm used for JWT signing (default: HS256)
   - `CORS_ALLOWED_ORIGINS`: Comma-separated list of allowed origins
   - `APP_ENV`: Environment (development, production, test)

## Database Setup

1. Run database migrations:
   ```bash
   alembic upgrade head
   ```

## Running the Application

### Development

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`.

### Production

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

All endpoints require a valid JWT token in the Authorization header:

```
Authorization: Bearer YOUR_JWT_TOKEN_HERE
```

### Task Management

- `GET /api/v1/{user_id}/tasks` - List user's tasks (with optional status filter)
- `POST /api/v1/{user_id}/tasks` - Create a new task
- `GET /api/v1/{user_id}/tasks/{task_id}` - Get specific task
- `PUT /api/v1/{user_id}/tasks/{task_id}` - Update task
- `DELETE /api/v1/{user_id}/tasks/{task_id}` - Delete task
- `PATCH /api/v1/{user_id}/tasks/{task_id}/complete` - Toggle completion status

### Health Checks

- `GET /health` - General health check
- `GET /health/database` - Database connectivity check

## Filtering Tasks

The `GET /api/v1/{user_id}/tasks` endpoint supports filtering by status:
- `/api/v1/{user_id}/tasks?status=all` - All tasks (default)
- `/api/v1/{user_id}/tasks?status=pending` - Pending tasks only
- `/api/v1/{user_id}/tasks?status=completed` - Completed tasks only

## Authentication & Authorization

- All API endpoints require a valid JWT token in the Authorization header
- The user ID in the JWT token must match the user ID in the URL path
- Invalid or missing tokens result in `401 Unauthorized`
- User ID mismatches result in `403 Forbidden`

## Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/unit/test_crud.py
```

## Configuration

The application uses environment variables for configuration:

- `DATABASE_URL`: Database connection string
- `BETTER_AUTH_SECRET`: Secret for JWT verification
- `JWT_ALGORITHM`: JWT algorithm (default: HS256)
- `CORS_ALLOWED_ORIGINS`: Comma-separated list of allowed origins
- `APP_ENV`: Application environment (default: development)

## Error Responses

All error responses follow this format:
```json
{
  "detail": "Error message"
}
```

## Performance Monitoring

The application includes performance monitoring via the `X-Process-Time` header in responses, indicating the time taken to process each request.

## Contributing

1. Create a feature branch
2. Make your changes
3. Add tests if applicable
4. Run tests to ensure everything works
5. Submit a pull request

## License

[License information goes here]