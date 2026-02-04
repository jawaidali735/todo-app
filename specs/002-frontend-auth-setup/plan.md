# Implementation Plan: Frontend & Authentication Setup (Next.js 16+)

**Branch**: `002-frontend-auth-setup` | **Date**: 2026-01-19 | **Spec**: specs/002-frontend-auth-setup/spec.md
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of a modern web application frontend using Next.js 16+ with Better Auth for authentication and Drizzle ORM for database interactions. The system will provide secure user signup/login functionality, protected dashboard access, and JWT-based communication with backend services.

## Technical Context

**Language/Version**: JavaScript/TypeScript with Next.js 16+ (App Router)
**Primary Dependencies**: Next.js, Better Auth, Drizzle ORM, @neondatabase/serverless, Tailwind CSS
**Storage**: Neon Serverless PostgreSQL database
**Testing**: Jest/React Testing Library (to be implemented)
**Target Platform**: Web browsers (Chrome, Firefox, Safari, Edge)
**Project Type**: Web application with frontend/backend separation
**Performance Goals**: Sub-3 second dashboard load time, responsive UI interactions
**Constraints**: JWT token security, user data isolation, responsive design across devices
**Scale/Scope**: Individual user accounts with secure data isolation

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Spec-Driven Development (SDD): Following specification from spec.md
- AI-Native Architecture: Using MCP tools (Context-7) for research and implementation
- Multi-User Data Isolation: Implementation will ensure users can only access their own data
- Single Source of Truth: Following constitution standards for Next.js 16+, Better Auth, Drizzle ORM
- Statelessness with JWT Authentication: Using Better Auth JWT plugin for stateless authentication

## Project Structure

### Documentation (this feature)

```text
specs/002-frontend-auth-setup/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
frontend/
├── src/
│   ├── app/
│   │
│   │   ├── api/
│   │   │   └── auth/
│   │   │       └── [...all]/
│   │   │           └── route.ts
│   │   │               # 🔗 BetterAuth ENTRY POINT
│   │   │               # Imports auth instance from lib/auth.ts
│   │   │               # Handles all /api/auth/* requests
│   │   │
│   │   ├── (auth)/
│   │   │   ├── layout.tsx
│   │   │   │   # 🔗 Shared layout for auth pages
│   │   │   │   # Wraps login and signup pages
│   │   │
│   │   │   ├── login/
│   │   │   │   └── page.tsx
│   │   │   │       # 🔗 Login page UI
│   │   │   │       # Uses components/auth/login-form.tsx
│   │   │   │       # Calls signIn via lib/auth-client.ts
│   │   │
│   │   │   └── signup/
│   │   │       └── page.tsx
│   │   │           # 🔗 Signup page UI
│   │   │           # Uses components/auth/signup-form.tsx
│   │   │           # Calls signUp via lib/auth-client.ts
│   │   │
│   │   ├── dashboard/
│   │   │   └── page.tsx
│   │   │       # 🔗 Protected page
│   │   │       # Access controlled by middleware.ts
│   │   │
│   │   ├── page.tsx
│   │   │   # 🔗 ROOT PAGE (/)
│   │   │   # Checks session on the server
│   │   │   # Redirects:
│   │   │   #   - logged-in users → /dashboard
│   │   │   #   - logged-out users → /login
│   │   │
│   │   ├── globals.css
│   │   │   # 🔗 Global styles (Tailwind, base CSS)
│   │   │
│   │   └── layout.tsx
│   │       # 🔗 ROOT LAYOUT
│   │       # Defines <html>, <body>, providers, theme, etc.
│   │
│   ├── components/
│   │   ├── auth/
│   │   │   ├── login-form.tsx
│   │   │   │   # 🔗 Uses auth-client.ts → signIn()
│   │   │   └── signup-form.tsx
│   │   │       # 🔗 Uses auth-client.ts → signUp()
│   │   │
│   │   ├── dashboard/
│   │   │   # 🔗 Dashboard-specific UI components
│   │   │
│   │   └── ui/
│   │       # 🔗 Reusable UI components (buttons, inputs, modals)
│   │
│   ├── lib/
│   │   ├── auth.ts
│   │   │   # 🔗 BetterAuth SERVER configuration
│   │   │   # Drizzle adapter is configured here
│   │   │   # Imports db from db/drizzle.ts
│   │   │
│   │   ├── auth-client.ts
│   │   │   # 🔗 BetterAuth CLIENT instance
│   │   │   # Used only in browser components
│   │   │
│   │   └── utils.ts
│   │       # 🔗 Shared utility/helper functions
│   │
│   ├── db/
│   │   ├── drizzle.ts
│   │   │   # 🔗 Drizzle database connection
│   │   │   # Connects to Neon PostgreSQL
│   │   │
│   │   └── schema.ts
│   │       # 🔗 Drizzle schema definitions
│   │       # Tables for BetterAuth and app data
│   │
│   ├── types/
│   │   # 🔗 Shared TypeScript types
│   │
│   └── middleware.ts
│       # 🔗 Route protection (auth guard)
│       # Checks session before allowing access
│
├── drizzle.config.ts
│   # 🔗 Drizzle migration configuration
│   # Uses schema.ts and DATABASE_URL
│
├── public/
│
├── .env.example
│   # 🔗 Environment variable template
│   # DATABASE_URL
│   # BETTER_AUTH_SECRET
│
├── .env.local
│   # 🔗 Actual secrets (never commit)
│
├── next.config.js
├── package.json
├── tailwind.config.js
└── tsconfig.json

```

**Structure Decision**: Web application structure with dedicated frontend directory for Next.js application. Authentication flows will be handled in (auth) group, with protected dashboard in separate route group. Database configuration uses Drizzle ORM connecting to Neon PostgreSQL.

## Phase 0: Research

**Concurrent research approach**: Using context-7 MCP to verify Better Auth integration with Next.js 16 and JWT plugin implementation.

- Research Better Auth integration patterns with Next.js 16+ App Router
- Verify JWT Plugin implementation to ensure tokens are accessible for backend communication
- Investigate Drizzle ORM schema definition for Better Auth tables
- Confirm Neon PostgreSQL connection patterns with Drizzle

## Phase 1: Foundation & Architecture

### Foundation Setup
- Initialize `/frontend` directory with Next.js 16+ using App Router
- Install dependencies: `better-auth`, `drizzle-orm`, `@neondatabase/serverless`, `dotenv`, `tailwindcss`
- Setup `.env.local` for frontend-specific environment variables
- Configure Tailwind CSS for styling

### Database Schema Definition
- Define database schema using Drizzle ORM for:
  - Better Auth tables (users, sessions, accounts, verification tokens)
  - Tasks table with user_id foreign key reference
- Sync schema with Neon DB using `drizzle-kit push`

## Phase 2: Authentication Implementation

### Better Auth Configuration
- Configure Better Auth with JWT plugin for stateless authentication
- Set up auth provider and client-side hooks
- Implement session management and token handling

### UI Implementation
- Create Auth UI components (Login/Signup forms)
- Implement Protected Dashboard layout with route protection
- Set up middleware for authentication checks

## Phase 3: Integration & API Communication

### Backend Communication Logic
- Implement API service layer to communicate with FastAPI backend
- Ensure all requests include `Authorization: Bearer <JWT_TOKEN>` header
- Create utility functions to retrieve JWT from Better Auth session

## Phase 4: Testing & Validation

### Quality Validation
- **Validation 1:** Verify user can signup and data appears in Neon DB
- **Validation 2:** Confirm Middleware redirects unauthenticated users to `/login`
- **Validation 3:** Check Network tab to ensure `Authorization: Bearer <token>` is present in API requests
- **Validation 4:** Verify user data isolation (users can't access other users' data)

## Key Decisions

**Decision:** Frontend-only Better Auth implementation
- *Option:* Full-stack auth vs Frontend-only JWT
- *Tradeoff:* Frontend-only chosen to keep Backend (FastAPI) stateless as per Phase 2 requirements

**Decision:** Using Drizzle ORM on Frontend
- *Tradeoff:* Required for Better Auth's database interaction, while Backend will use SQLModel for data validation

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Multiple ORMs (Drizzle + SQLModel) | Better Auth requires Drizzle on frontend, SQLModel is constitutionally required for backend | Using single ORM would break Better Auth integration or violate backend standards |