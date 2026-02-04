# Feature Specification: Backend HTTP + DB Upgrade

**Feature Branch**: `003-backend-http-db`
**Created**: 2026-01-20
**Status**: Draft
**Input**: User description: "Backend upgrade — Phase II (Enhance Phase-I backend into HTTP + DB)

Target audience: Backend developers, real world users of todo and tech engineers etc
Focus: Enhance existing Phase-I terminal/in-memory backend logic into a FastAPI service with JWT middleware, per-user isolation, and real PostgreSQL (Neon) persistence. Frontend will communicate exclusively via HTTP APIs and all task data must be stored and retrieved from the database.

Success criteria:
- Phase-I backend logic is reused and enhanced (not rewritten) and exposed through REST APIs.
- Frontend sends JWT with every request; backend verifies JWT using middleware and identifies the authenticated user.
- Backend uses the SAME `BETTER_AUTH_SECRET` as frontend to verify JWT.
- All task operations (create, read, update, delete, complete) persist data in PostgreSQL.
- Backend returns only the authenticated user's tasks (strict user isolation).
- All endpoints return correct HTTP status codes and JSON responses.
- Unit and integration tests validate JWT handling, user filtering, and CRUD behavior.

Constraints:
- Must extend the existing Phase-I `/backend` folder and logic originally built for terminal use.
- Must convert in-memory storage into database-backed persistence.
- Tech stack: Python, FastAPI, SQLModel (or SQLAlchemy), PostgreSQL (Neon), Alembic migrations.
- Backend must NOT call Better Auth APIs; JWT verification must be local.
- JWT must be verified using `BETTER_AUTH_SECRET`, shared with frontend.
- All APIs must be under `/api/v1`.
- Environment variables required: `DATABASE_URL`, `BETTER_AUTH_SECRET`, `CORS_ALLOWED_ORIGINS`, `APP_ENV`.

Authentication & user identification:
- Frontend sends `Authorization: Bearer <JWT>` with every API request.
- Backend middleware must:
  - Extract JWT from request headers.
  - Verify JWT signature using `BETTER_AUTH_SECRET`.
  - Decode JWT payload and extract user identifier (e.g. `user_id` or `sub`).
  - Attach authenticated user to request context.
  - Reject missing or invalid tokens with `401 Unauthorized`.
  - Reject requests where URL `{user_id}` does not match JWT user with `403 Forbidden`.

Functional requirements:
- `POST   /api/v1/{user_id}/tasks` — Create a new task for authenticated user.
- `GET    /api/v1/{user_id}/tasks` — List tasks for authenticated user (filters: all/pending/completed).
- `GET    /api/v1/{user_id}/tasks/{task_id}` — Retrieve a single task.
- `PUT    /api/v1/{user_id}/tasks/{task_id}` — Update task title/description.
- `PATCH  /api/v1/{user_id}/tasks/{task_id}/complete` — Mark task complete/incomplete.
- `DELETE /api/v1/{user_id}/tasks/{task_id}` — Delete a task.

Data model:
- tasks table:
  - id (UUID, primary key)
  - user_id (TEXT or UUID, indexed)
  - title (VARCHAR, max 200)
  - description (TEXT, optional)
  - completed (BOOLEAN)
  - created_at (TIMESTAMP)
  - updated_at (TIMESTAMP)
- Indexes:
  - tasks.user_id
  - tasks(user_id, completed)

Middleware requirements:
- JWT verification middleware or dependency is mandatory.
- Middleware must be"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Secure Task Management via HTTP APIs (Priority: P1)

As a user of the todo app, I want to securely create, read, update, and delete my tasks through HTTP APIs that authenticate me with JWT tokens, so that my task data is isolated from other users and persisted in a reliable database.

**Why this priority**: This is the core functionality of the todo app and enables secure multi-user access to task data with proper persistence.

**Independent Test**: Can be fully tested by authenticating with a JWT token and performing all CRUD operations on tasks, delivering complete task management functionality with user isolation.

**Acceptance Scenarios**:

1. **Given** I am an authenticated user with a valid JWT token, **When** I make HTTP requests to the task endpoints with my user_id in the URL, **Then** I can only access, modify, or delete my own tasks and receive proper HTTP status codes and JSON responses.

2. **Given** I have an expired or invalid JWT token, **When** I attempt to access task endpoints, **Then** I receive a 401 Unauthorized response preventing unauthorized access.

3. **Given** I attempt to access another user's tasks by changing the user_id in the URL, **When** my JWT contains a different user identifier, **Then** I receive a 403 Forbidden response maintaining proper user isolation.

---

### User Story 2 - Task Operations with Database Persistence (Priority: P1)

As a backend developer, I want the system to store and retrieve task data from PostgreSQL instead of in-memory storage, so that data persists across application restarts and scales appropriately for multiple users.

**Why this priority**: Database persistence is essential for a production-ready application where data loss cannot be tolerated.

**Independent Test**: Can be fully tested by creating tasks, restarting the application, and verifying that the tasks still exist, delivering reliable data persistence.

**Acceptance Scenarios**:

1. **Given** I am an authenticated user creating a task, **When** the task is saved to the database, **Then** the task persists and can be retrieved after application restarts.

2. **Given** I am an authenticated user modifying a task, **When** the update is processed, **Then** the changes are reflected in the database and returned in subsequent queries.

---

### User Story 3 - JWT-Based Authentication Flow (Priority: P2)

As a tech engineer implementing the frontend, I want to send JWT tokens in the Authorization header with every API request, so that the backend can verify my identity and provide appropriate access to resources.

**Why this priority**: Proper authentication flow is critical for security and enables the separation of concerns between frontend and backend.

**Independent Test**: Can be fully tested by sending various JWT tokens with API requests and verifying that the middleware properly validates or rejects them, delivering secure authentication.

**Acceptance Scenarios**:

1. **Given** I have a valid JWT token with user identity, **When** I make an API request with the Authorization header, **Then** the middleware extracts and validates my user identity allowing appropriate access.

2. **Given** I send a malformed or missing Authorization header, **When** I make an API request, **Then** I receive a 401 Unauthorized response.

---

### Edge Cases

- What happens when the database connection fails during a request?
- How does the system handle JWT tokens with invalid signatures or expired timestamps?
- What occurs when a user attempts to access a task that doesn't belong to them?
- How does the system behave when database indexes are missing or corrupted?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST expose REST API endpoints under `/api/v1` for task management operations
- **FR-002**: System MUST verify JWT tokens using the `BETTER_AUTH_SECRET` shared with the frontend
- **FR-003**: System MUST extract user identifier from JWT payload and enforce user isolation
- **FR-004**: System MUST persist task data in PostgreSQL database with proper indexing
- **FR-005**: System MUST reject requests with invalid or missing JWT tokens with 401 status
- **FR-006**: System MUST reject requests where URL user_id doesn't match JWT user with 403 status
- **FR-007**: System MUST support all CRUD operations on tasks: create, read, update, delete, complete
- **FR-008**: System MUST return appropriate HTTP status codes and JSON responses
- **FR-009**: System MUST reuse existing Phase-I backend logic and enhance it for HTTP use
- **FR-010**: System MUST include unit and integration tests for JWT handling and CRUD operations

### Key Entities *(include if feature involves data)*

- **Task**: Represents a user's task with properties: id (UUID), user_id (TEXT/UUID), title (VARCHAR), description (TEXT), completed (BOOLEAN), created_at (TIMESTAMP), updated_at (TIMESTAMP)
- **User**: Represents an authenticated user identified by their unique user_id extracted from JWT claims
- **JWT Token**: Authentication token containing user identity that must be verified using `BETTER_AUTH_SECRET`

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can perform all task operations (create, read, update, delete, complete) with proper authentication and receive appropriate HTTP responses within 500ms
- **SC-002**: System maintains strict user isolation where users can only access their own tasks with 100% accuracy
- **SC-003**: All task data persists reliably in PostgreSQL database and survives application restarts
- **SC-004**: 95% of API requests with valid JWT tokens are processed successfully while invalid tokens are rejected with appropriate error codes
- **SC-005**: Unit and integration tests achieve 80% code coverage for JWT handling, user filtering, and CRUD operations