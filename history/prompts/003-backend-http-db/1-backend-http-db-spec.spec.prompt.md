---
id: 1
title: backend-http-db-spec
stage: spec
date_iso: 2026-01-20
surface: agent
model: claude-sonnet-4-5-20250929
feature: 003-backend-http-db
branch: 003-backend-http-db
user: user
command: /sp.specify Backend upgrade — Phase II (Enhance Phase-I backend into HTTP + DB)
labels: ["spec", "backend", "authentication", "database"]
spec: null
ticket: null
adr: null
pr: null
---

# Prompt History Record: backend-http-db-spec

## Files Modified

 - specs/003-backend-http-db/spec.md
 - specs/003-backend-http-db/checklists/requirements.md

## Tests Performed

 - Created specification document with user scenarios
 - Validated requirements and success criteria
 - Generated quality checklist

## Prompt Text

```
Backend upgrade — Phase II (Enhance Phase-I backend into HTTP + DB)

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
- Middleware must be
```

## Response Text

Created a comprehensive specification for the backend HTTP + DB upgrade feature. The specification includes:

1. User scenarios covering secure task management, database persistence, and JWT authentication flow
2. Functional requirements defining the system capabilities
3. Key entities representing the data structures
4. Success criteria with measurable outcomes

The spec defines requirements for exposing REST APIs under /api/v1, verifying JWT tokens, enforcing user isolation, persisting data in PostgreSQL, and maintaining proper authentication flows. It also includes acceptance scenarios and edge cases to ensure comprehensive test coverage.

A quality checklist was also created to validate the specification's completeness.