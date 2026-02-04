# Research: Backend HTTP + DB Upgrade

## Decision: JWT Handling Approach
**Rationale**: The specification requires local JWT verification using the shared `BETTER_AUTH_SECRET` rather than calling external auth services. This approach provides better performance and reduces external dependencies while maintaining security.
**Alternatives considered**:
- Calling external Better Auth APIs (rejected - adds network latency and dependency)
- Session-based authentication (rejected - violates statelessness requirement)

## Decision: Database Migration Strategy
**Rationale**: Using Alembic for database migrations provides safe, version-controlled schema evolution with rollback capabilities. This is essential for production deployments.
**Alternatives considered**:
- Runtime table creation (rejected - no rollback capability, unsafe for production)
- Manual SQL scripts (rejected - lacks version control and automation)

## Decision: ORM Selection
**Rationale**: SQLModel is chosen as it combines the power of SQLAlchemy with Pydantic validation, providing type safety and data validation while supporting complex queries needed for user isolation.
**Alternatives considered**:
- Raw SQL (rejected - vulnerable to injection, no type safety)
- SQLAlchemy Core only (rejected - lacks validation features)
- Peewee (rejected - less mature than SQLModel/SQLAlchemy)

## Decision: Phase-I Logic Integration
**Rationale**: The existing Phase-I terminal logic will be refactored into the CRUD layer, separating business logic from presentation concerns while maintaining functionality.
**Approach**: Extract validation rules and business logic from terminal version, adapt for HTTP context and database persistence.

## JWT Payload Structure Research
Based on Better Auth documentation, JWT tokens contain:
- `sub`: Subject (user ID)
- `email`: User email
- `exp`: Expiration timestamp
- `iat`: Issued at timestamp
- Additional custom claims may be present

The middleware will extract the user ID from the `sub` claim to enforce user isolation.

## FastAPI Security Implementation
FastAPI's dependency injection system will be used to inject the authenticated user context into route handlers, ensuring consistent access to user identity across all endpoints.

## Database Connection Pooling
Using SQLModel's recommended connection pooling approach with PostgreSQL to handle concurrent requests efficiently while managing database resources.