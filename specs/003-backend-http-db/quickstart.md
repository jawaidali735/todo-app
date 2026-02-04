# Backend Quickstart Guide

## Prerequisites

- Python 3.11+
- PostgreSQL database (Neon Serverless recommended)
- Better Auth secret key

## Setup

1. **Clone the repository and navigate to the backend directory**
   ```bash
   cd backend
   ```

2. **Install dependencies using uv (recommended)**
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install -r requirements.txt
   ```

3. **Create environment file**
   ```bash
   cp .env.example .env
   ```

4. **Configure environment variables**
   ```bash
   # Edit .env file
   DATABASE_URL="postgresql://username:password@localhost:5432/todo_db"
   BETTER_AUTH_SECRET="your-secret-key-here"
   JWT_ALGORITHM="HS256"
   CORS_ALLOWED_ORIGINS="http://localhost:3000,https://yourdomain.com"
   APP_ENV="development"
   ```

5. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

6. **Start the development server**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## API Usage

### Authentication
All API endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer YOUR_JWT_TOKEN_HERE
```

### Available Endpoints

#### Task Management
- `GET /api/v1/{user_id}/tasks` - List user's tasks
- `POST /api/v1/{user_id}/tasks` - Create a new task
- `GET /api/v1/{user_id}/tasks/{task_id}` - Get specific task
- `PUT /api/v1/{user_id}/tasks/{task_id}` - Update task
- `DELETE /api/v1/{user_id}/tasks/{task_id}` - Delete task
- `PATCH /api/v1/{user_id}/tasks/{task_id}/complete` - Toggle completion status

### Example Requests

**Create a task:**
```bash
curl -X POST http://localhost:8000/api/v1/user123/tasks \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn FastAPI", "description": "Build a sample app"}'
```

**Get all tasks:**
```bash
curl -X GET http://localhost:8000/api/v1/user123/tasks \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Development

### Running Tests
```bash
pytest
```

### Running Tests with Coverage
```bash
pytest --cov=app
```

### Creating New Migrations
```bash
alembic revision --autogenerate -m "Description of changes"
alembic upgrade head
```

### API Documentation
The API documentation is available at:
- `/docs` - Interactive Swagger UI
- `/redoc` - ReDoc documentation

## Project Structure
```
backend/
├── app/                    # Main application
│   ├── main.py            # Application entry point
│   ├── core/              # Core functionality (auth, config)
│   ├── api/               # API route definitions
│   ├── models/            # Database models
│   ├── crud/              # Database operations
│   └── db/                # Database configuration
├── alembic/               # Database migrations
├── tests/                 # Test files
└── requirements.txt       # Python dependencies
```

## Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
- `BETTER_AUTH_SECRET`: Secret key for JWT verification (must match frontend)
- `JWT_ALGORITHM`: Algorithm used for JWT signing (default: HS256)
- `CORS_ALLOWED_ORIGINS`: Comma-separated list of allowed origins
- `APP_ENV`: Environment (development, production, test)