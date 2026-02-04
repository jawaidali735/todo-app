---
id: 2
title: backend-http-db-plan
stage: plan
date_iso: 2026-01-20
surface: agent
model: claude-sonnet-4-5-20250929
feature: 003-backend-http-db
branch: 003-backend-http-db
user: user
command: /sp.plan Backend upgrade — Phase II (Enhance Phase-I backend into HTTP + DB)
labels: ["plan", "backend", "architecture", "api"]
spec: ../spec.md
ticket: null
adr: null
pr: null
---

# Prompt History Record: backend-http-db-plan

## Files Modified

 - specs/003-backend-http-db/plan.md
 - specs/003-backend-http-db/research.md
 - specs/003-backend-http-db/data-model.md
 - specs/003-backend-http-db/contracts/openapi.yaml
 - specs/003-backend-http-db/quickstart.md

## Tests Performed

 - Created implementation plan with technical context
 - Researched JWT handling and database migration approaches
 - Defined data models for tasks and users
 - Created API contracts (OpenAPI specification)
 - Generated quickstart guide for developers

## Prompt Text

```
Backend upgrade — Phase II (Enhance Phase-I backend into HTTP + DB)

Create:
- Backend-only architecture sketch covering API layer, JWT middleware, business logic, and database.
- Clear backend code structure derived from Phase-I terminal backend.
- Step-by-step implementation plan to evolve in-memory logic into DB-backed REST APIs.
- Quality validation strategy strictly mapped to backend success criteria.

Architecture sketch:
- FastAPI application exposing REST endpoints under `/api/v1`.
- Mandatory JWT verification middleware executed before any route logic.
- Middleware verifies JWT using `BETTER_AUTH_SECRET` and extracts authenticated user ID.
- Authenticated user ID is injected into request context.
- API routes call backend business logic functions (ported from Phase-I).
- Business logic performs CRUD operations against PostgreSQL (Neon) via ORM.
- Database persists tasks with strict per-user isolation.

Section structure (backend code organization):
- `app/main.py` — FastAPI app initialization and router registration.
- `app/core/auth.py` — JWT verification middleware / dependency.
- `app/api/tasks.py` — Task CRUD API routes.
- `app/crud.py` — Business logic (enhanced Phase-I terminal logic).
- `app/models.py` — ORM models.
- `app/db.py` — Database engine and session management.
- `alembic/` — Database migration scripts.
- `tests/` — Backend unit and integration tests.

Research approach:
- Research-concurrent approach:
  - Analyze Phase-I backend logic while designing database models.
  - Inspect JWT payload structure during middleware implementation.
  - Validate database schema while writing migrations and CRUD functions.
- Avoid upfront over-design; refine architecture based on backend constraints.

Implementation phases:

Phase 1 — Research
- Review existing Phase-I `/backend` terminal logic.
- Identify reusable functions and validation rules.
- Document data flow in Phase-I (task creation, update, delete, completion).
- Determine user identifier field extracted from JWT.

Phase 2 — Foundation
- Initialize FastAPI backend structure.
- Configure database connection using environment variables.
- Implement ORM models for tasks.
- Create JWT verification middleware using `BETTER_AUTH_SECRET`.
- Ensure authenticated user is available in request context.

Phase 3 — Analysis
- Port Phase-I logic into reusable CRUD functions.
- Replace in-memory data handling with database persistence.
- Implement REST endpoints calling CRUD layer.
- Enforce user filtering in all database queries.
- Add Alembic migrations for schema creation and indexing.

Phase 4 — Synthesis
- Implement unit tests for ported Phase-I logic.
- Implement integration tests for API endpoints.
- Validate authentication, authorization, and error handling.
- Finalize backend documentation and setup instructions.

Decisions needing documentation:
- JWT handling:
  - Option A: Verify JWT locally using shared secret.
  - Option B: Call external auth service.
  - Decision: Option A — local verification with `BETTER_AUTH_SECRET`.
- Persistence layer:
  - Option A: Continue in-memory storage.
  - Option B: Database-backed storage.
  - Decision: Option B — PostgreSQL persistence required.
- Migration strategy:
  - Option A: Runtime table creation.
  - Option B: Alembic migrations.
  - Decision: Option B — explicit migrations for safety.

Testing strategy:
- Unit tests:
  - Validate Phase-I business rules remain intact.
  - Test CRUD functions independently.
- Integration tests:
  - JWT valid → request processed.
  - JWT missing/invalid → `401 Unauthorized`.
  - JWT user mismatch → `403 Forbidden`.
  - CRUD operations persist and retrieve correct data.
- Regression checks:
  - Confirm no task data leaks across users.

Quality validation:
- Each success criterion in `/sp.specify` mapped to at least one test.
- Code review checklist ensures:
  - JWT user is never trusted from request body or params.
  - All DB queries filter by authenticated user.
  - Phase-I logic reuse is explicit and documented.
- CI pipeline runs t
```

## Response Text

Completed the implementation plan for the backend HTTP + DB upgrade. Created the following artifacts:

1. Implementation plan (plan.md) - Outlined the technical approach and project structure
2. Research document (research.md) - Resolved technical decisions about JWT handling, database migrations, and ORM selection
3. Data model (data-model.md) - Defined the Task entity and database schema with security constraints
4. API contracts (contracts/openapi.yaml) - Created OpenAPI specification for all endpoints
5. Quickstart guide (quickstart.md) - Provided setup instructions and usage examples

The plan follows the architecture sketch provided in the user input, organizing the backend with FastAPI, JWT middleware, and SQLModel ORM. It ensures user isolation by validating JWT tokens and filtering database queries by user_id. The implementation will reuse Phase-I logic while converting in-memory operations to database-persisted operations.