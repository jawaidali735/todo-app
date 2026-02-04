# Implementation Plan: Backend HTTP + DB Upgrade

**Branch**: `003-backend-http-db` | **Date**: 2026-01-20 | **Spec**: [link](../spec.md)
**Input**: Feature specification from `/specs/003-backend-http-db/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Upgrade the existing Phase-I terminal/in-memory backend to a FastAPI HTTP service with JWT authentication middleware and PostgreSQL persistence. The system will expose REST APIs under `/api/v1`, verify JWT tokens using `BETTER_AUTH_SECRET`, enforce user isolation, and persist task data to Neon PostgreSQL database.

## Technical Context

**Language/Version**: Python 3.11
**Primary Dependencies**: FastAPI, SQLModel, PyJWT, psycopg2-binary, python-multipart, uvicorn
**Storage**: PostgreSQL (Neon Serverless)
**Testing**: pytest with FastAPI test client
**Target Platform**: Linux/Mac/Windows server
**Project Type**: Web backend service
**Performance Goals**: Sub-500ms API response times, support 1000+ concurrent users
**Constraints**: Must reuse Phase-I logic, enforce user isolation, validate JWT locally
**Scale/Scope**: Multi-user SaaS application with secure data isolation

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- ✅ **Spec-Driven Development**: Following SDD sequence (Spec → Plan → Tasks → Code)
- ✅ **AI-Native Architecture**: Using Claude Code for implementation
- ✅ **Multi-User Data Isolation**: Enforcing user isolation via JWT verification and user_id filtering
- ✅ **Statelessness with JWT**: Using JWT tokens for stateless authentication
- ✅ **Tech Stack Compliance**: Using FastAPI, SQLModel, PostgreSQL as required
- ✅ **Authentication Requirements**: Implementing JWT verification with BETTER_AUTH_SECRET
- ✅ **Database Schema**: Creating tasks table with user_id foreign key for isolation
- ✅ **API Design Standards**: Implementing RESTful endpoints with proper HTTP status codes
- ✅ **Security Requirements**: Requiring JWT for all endpoints, 401/403 responses for invalid access

## Project Structure

### Documentation (this feature)

```text
specs/003-backend-http-db/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI app initialization and router registration
│   ├── core/
│   │   ├── __init__.py
│   │   ├── auth.py      # JWT verification middleware / dependency
│   │   └── config.py    # Configuration and environment variables
│   ├── api/
│   │   ├── __init__.py
│   │   └── tasks.py     # Task CRUD API routes
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py      # ORM models
│   ├── crud/
│   │   ├── __init__.py
│   │   └── task.py      # Business logic (enhanced Phase-I terminal logic)
│   ├── db/
│   │   ├── __init__.py
│   │   └── database.py  # Database engine and session management
│   └── utils/
│       ├── __init__.py
│       └── validators.py # Validation utilities
├── alembic/
│   ├── versions/        # Migration files
│   └── env.py           # Alembic configuration
├── alembic.ini          # Alembic settings
├── requirements.txt     # Python dependencies
├── pyproject.toml       # Project configuration
└── tests/
    ├── __init__.py
    ├── conftest.py      # Test fixtures
    ├── unit/
    │   ├── __init__.py
    │   └── test_crud.py # Unit tests for CRUD functions
    └── integration/
        ├── __init__.py
        └── test_api.py  # Integration tests for API endpoints
```

**Structure Decision**: Web backend service with FastAPI, following the architecture sketch provided in the user input. Organized into logical modules: main app, core (auth/config), API routes, models, CRUD operations, database management, and utilities.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Multiple modules | Modularity and separation of concerns | Single-file approach would be difficult to maintain |