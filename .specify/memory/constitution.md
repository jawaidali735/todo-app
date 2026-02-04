<!-- SYNC IMPACT REPORT:
Version change: 4.0.0 → 5.0.0
Modified principles: Spec-Driven Development, Tech Stack, Project Structure
Added sections: Phase 2 Standards, Frontend & Auth Spec, Backend & API Spec
Removed sections: Old UI/UX Standards, Old API Design Standards
Templates requiring updates: ✅ Updated plan-template.md, ✅ Updated spec-template.md, ✅ Updated tasks-template.md
Follow-up TODOs: None
-->
# Full-Stack AI-Powered Todo Application Constitution (Phase 2)

## Core Principles

### Spec-Driven Development (SDD)
All development must be driven by specifications. No manual coding; Claude Code must implement features based on provided specs. Implementation follows the sequence: Specification → Plan → Tasks → Code.

### AI-Native Architecture
Utilize Spec-Kit Plus and MCP tools (Context-7) for research and implementation. Leverage AI tools for all development activities including code generation, research, and documentation.

### Multi-User Data Isolation
Every user must have a private data space. No user should be able to access another user's tasks. The system must enforce strict user data separation to ensure privacy and security.

### Single Source of Truth
All project standards and technical choices are governed by this constitution. All subsequent development artifacts (specs, plans, tasks) must align with these principles.

### Statelessness with JWT Authentication
The application must use stateless architecture with JWT tokens enabling scalable, session-free backend operations. No server-side session storage is allowed. Authentication must be handled through Better Auth with JWT plugin.

## Development Governance

### Development Approach (NON-NEGOTIABLE):
- Agentic Dev Stack only
- Workflow:
  1. Write Specification
  2. Generate Plan
  3. Break into Tasks
  4. Implement via Claude Code
- Manual coding is strictly forbidden
- No implementation without an approved spec
- If requirements are unclear, the agent must STOP and request a spec update

### Hierarchy of Authority:
Constitution > Specification > Plan > Tasks > Code

### Amendment Procedure:
Changes to this constitution require explicit approval and must update the version number according to semantic versioning:
- MAJOR: Backward incompatible governance/principle removals
- MINOR: New principle/section added
- PATCH: Clarifications, wording, typo fixes

## Tech Stack (Phase 2 Standards)

### Frontend Requirements:
- **Framework:** Next.js 16+ (App Router only, not Pages Router)
- **Styling:** Tailwind CSS
- **Icons:** Lucide React Icons
- **Type Safety:** TypeScript strict mode
- **Authentication:** Better Auth integration with JWT plugin
- **ORM:** Drizzle ORM for database schema management
- **Database Driver:** @neondatabase/serverless for Neon Serverless PostgreSQL

### Backend Requirements:
- **Framework:** Python FastAPI
- **Database:** Neon Serverless PostgreSQL
- **ORM:** SQLModel for professional API development and data validation
- **Environment Management:** uv for dependency management
- **Type Hints:** All endpoints must use proper type annotations

### Database Requirements:
- **Provider:** Neon Serverless PostgreSQL
- **ORM Tools:** Drizzle ORM (Frontend) and SQLModel (Backend)
- **Schema:** Must support Users and Tasks tables with proper relationships

### Authentication Requirements:
- **Provider:** Better Auth with JWT Plugin enabled for cross-platform communication
- **Token Format:** JWT for stateless authentication
- **Security:** Password hashing with bcrypt, secure token validation
- **Cross-Platform:** JWT tokens must work across frontend and backend

## Project Structure & Specs

### Phase 1: Frontend & Auth Spec
- **Directory:** `frontend/`
- **Auth Setup:** Integrate Better Auth using MCP (Context-7) documentation with JWT support enabled
- **Database Config:** Install `drizzle-orm @neondatabase/serverless` and `drizzle-kit`. Configure schema for Users and Tasks
- **UI/UX:** Build a professional dashboard with task management (Add, View, Stats, Update, Delete) using Tailwind CSS
- **Integration:** Ensure all API calls include the `Authorization: Bearer <JWT>` header
- **Code Quality:** TypeScript strict mode, component reusability, proper error handling

### Phase 2: Backend & API Spec
- **Directory:** `backend/`
- **Environment:** Initialize using `uv` for proper Python environment management
- **API Implementation:** Develop RESTful endpoints (`GET`, `POST`, `PUT`, `DELETE`, `PATCH`) using SQLModel
- **Security:** Implement a middleware to verify Better Auth JWT tokens and extract the `user_id` to filter database queries
- **Data Validation:** Use SQLModel for schema validation and type safety
- **Documentation:** Auto-generated API documentation with FastAPI's built-in Swagger UI

## Environment Configuration

### Frontend (.env.local):
- `NEXT_PUBLIC_BETTER_AUTH_URL`
- `NEXT_PUBLIC_BETTER_AUTH_SECRET`
- `NEXT_PUBLIC_API_BASE_URL`
- `NEXT_PUBLIC_AUTH_ENABLED`

### Backend (.env):
- `DATABASE_URL` (Neon PostgreSQL connection string)
- `BETTER_AUTH_SECRET`
- `JWT_ALGORITHM`
- `JWT_EXPIRATION_DAYS`
- `CORS_ORIGINS`

### Environment File Requirements:
- Both frontend and backend must have identical `BETTER_AUTH_SECRET`
- All .env files must be in .gitignore to prevent committing secrets
- Provide .env.example templates with placeholder values
- Frontend uses .env.local, backend uses .env (both excluded from Git)

## API Design Standards

### Authentication :
- sign in and sign out sesssion etc will be sued in frontend
- betterauth has buuiltedn fucntion of so use that.

### Task Management Endpoints (JWT required):
- GET /api/{user_id}/tasks - List user's tasks
- POST /api/{user_id}/tasks - Create new task
- GET /api/{user_id}/tasks/{id} - Retrieve specific task
- PUT /api/{user_id}/tasks/{id} - Update task
- DELETE /api/{user_id}/tasks/{id} - Delete task
- PATCH /api/{user_id}/tasks/{id}/complete - Toggle task completion

### API Design Principles:
- RESTful conventions with proper HTTP status codes (200, 201, 400, 401, 403, 404, 500)
- Explicit request and response schemas
- Predictable error responses
- Consistent JSON formatting
- Proper validation and sanitization

## Authentication & Security

### JWT Flow (MANDATORY):
1. User authenticates on frontend using Better Auth
2. Better Auth creates session and issues JWT token with user_id
3. Frontend includes token in every API request: `Authorization: Bearer <token>`
4. Backend extracts token from request header
5. Backend verifies token signature using shared BETTER_AUTH_SECRET
6. Backend decodes token to obtain user_id and email
7. Backend matches decoded user_id with URL parameters
8. Backend filters all Todo tasks by authenticated user_id

### Security Requirements:
- ALL API endpoints require valid JWT (except auth endpoints)
- Requests without JWT → 401 Unauthorized
- Requests with invalid JWT → 401 Unauthorized
- User ID in URL must match JWT user ID → 403 Forbidden if mismatch
- Password hashing: bcrypt or passlib (never plain text)
- JWT signing: HS256 with BETTER_AUTH_SECRET from .env
- User isolation: All queries filtered by authenticated user_id
- CORS: Configure from CORS_ORIGINS environment variable

## Database Schema Requirements

### Users Table:(frontend ORM table in neon)
- id (Primary Key, UUID/string)
- email (Unique, indexed)
- password_hash (hashed with bcrypt)
- name (optional)
- created_at (timestamp)

### Tasks Table:
- id (Primary Key, UUID/string)
- user_id (Foreign Key to users.id, indexed)
- title (string, not null)
- description (text, optional)
- completed (boolean, default false)
- created_at (timestamp)
- updated_at (timestamp)

### Relationships:
- Foreign key constraint: tasks.user_id → users.id (CASCADE delete)
- Indexes on user_id for efficient querying
- Index on completed status for filtering

## UI/UX Standards

### Primary UI Goal:
Build a **beautiful, professional Todo application dashboard**

### UI Requirements:
- Modern, clean, visually appealing design
- Professional SaaS aesthetic (Linear/Notion/Vercel style)
- Clear task list visualization with distinct completed/pending states
- Smooth task creation and update interactions
- Clear loading, empty, and error states
- Fully responsive across devices (mobile-first approach)
- Auth-aware UI (no unauthenticated access to tasks)
- Loading states, smooth transitions, hover effects
- Accessibility: ARIA labels, keyboard navigation, proper contrast
- Error handling: Clear validation messages

## Code Quality Standards

### Frontend Standards:
- TypeScript strict mode with proper type definitions
- Component reusability and modularity
- Proper error handling and loading states
- Clean, maintainable code structure
- Proper separation of concerns

### Backend Standards:
- Python type hints on all functions
- Comprehensive docstrings
- Proper error handling and logging
- Input validation and sanitization
- Efficient database queries with proper indexing

### General Standards:
- Proper HTTP status codes
- Consistent JSON responses
- Secure authentication and authorization
- Proper environment variable usage
- No hardcoded secrets or credentials

## Success Criteria

### Phase 1 (Frontend & Auth):
- Professional Next.js 16+ dashboard with Tailwind CSS
- Better Auth integration with JWT support
- Drizzle ORM schema for Users and Tasks
- Task management UI (Add, View, Stats, Update, Delete)
- Proper authentication flow

### Phase 2 (Backend & API):
- FastAPI backend with SQLModel ORM
- Complete RESTful API with all CRUD operations
- JWT-based authentication and authorization
- User data isolation and security
- Auto-generated API documentation

### Overall Success:
- Zero manual coding (Claude Code only)
- All specifications implemented according to Phase 1 and Phase 2 requirements
- Proper environment configuration with secure secret management
- Professional-quality UI/UX
- Complete API functionality with proper security
- Multi-user data isolation working correctly

## Constraints

- No manual coding outside of Claude Code and Spec-Kit Plus
- No hardcoded secrets (environment variables only)
- No SQL injection (proper ORM usage required)
- No insecure password storage (bcrypt/passlib required)
- No endpoints without proper JWT validation (except auth endpoints)
- No user_id mismatches between token and URL parameters
- No .env files committed to Git (must be in .gitignore)
- Identical BETTER_AUTH_SECRET in frontend vs backend
- Strict adherence to Next.js App Router (not Pages Router)
- Use of uv for Python environment management
- Proper separation of frontend and backend concerns

## Quality Assurance

- All code must pass type checking (TypeScript and Python)
- API endpoints must return proper HTTP status codes
- Database operations must use ORM (no raw SQL)
- Authentication must be validated on every secured endpoint
- Frontend must properly handle authentication states
- Error responses must be consistent and informative

## Governance

This constitution establishes the fundamental principles and constraints that govern all development decisions for the Full-Stack AI-Powered Todo Application. All code changes, feature additions, and architectural decisions must align with these principles. Any proposed changes that conflict with these principles require explicit amendment to the constitution with clear justification.

**Version**: 5.0.0 | **Ratified**: 2026-01-15 | **Last Amended**: 2026-01-19