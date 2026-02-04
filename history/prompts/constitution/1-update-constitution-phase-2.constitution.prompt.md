---
id: 1
title: "update-constitution-phase-2"
stage: "constitution"
date_iso: "2026-01-19"
surface: "agent"
model: "Claude Sonnet 4.5"
feature: "none"
branch: "master"
user: "user"
command: "sp.constitution"
labels: ["constitution", "spec-driven-development", "full-stack"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - ".specify/memory/constitution.md"
tests_yaml: []
---

# Constitution Update: Full-Stack AI-Powered Todo Application (Phase 2)

## Overview
Updated the project constitution to reflect Phase 2 standards for the Full-Stack AI-Powered Todo Application, focusing on Spec-Driven Development (SDD), AI-Native Architecture, Multi-User Data Isolation, and Single Source of Truth principles.

## Changes Made
- Completely revised the constitution to incorporate Phase 2 tech stack requirements
- Added detailed frontend requirements (Next.js 15+, Tailwind CSS, Better Auth, Drizzle ORM)
- Added detailed backend requirements (Python FastAPI, SQLModel, uv environment management)
- Defined clear project structure for two phases (Frontend & Auth, Backend & API)
- Enhanced security requirements with JWT flow and authentication standards
- Updated API design standards with comprehensive endpoint specifications
- Included database schema requirements for user isolation
- Established clear environment configuration standards

## Technical Details
- Version incremented from 4.0.0 to 5.0.0 (MAJOR update due to significant structural changes)
- New tech stack standards established for both frontend and backend
- Multi-user data isolation is now a core principle
- AI-Native Architecture with MCP tools integration emphasized
- Proper separation of concerns between frontend and backend defined

## Acceptance Criteria Met
- [x] All Phase 2 requirements documented in constitution
- [x] Clear distinction between Phase 1 (Frontend & Auth) and Phase 2 (Backend & API)
- [x] Tech stack requirements aligned with user specifications
- [x] Security and authentication requirements clearly defined
- [x] Environment configuration standards established
- [x] Proper governance and versioning procedures documented

## Outcome
The constitution now serves as the authoritative source for Phase 2 development of the Full-Stack AI-Powered Todo Application, providing clear guidelines for implementing both frontend and backend components with proper security, authentication, and user data isolation.

## Prompt Text
```
Full-Stack AI-Powered Todo Application (Phase 2)

## Core Principles
- **Spec-Driven Development (SDD):** All development must be driven by specifications. No manual coding; Claude Code must implement features based on provided specs.
- **AI-Native Architecture:** Utilize Spec-Kit Plus and MCP tools (Context-7) for research and implementation.
- **Multi-User Data Isolation:** Every user must have a private data space. No user should be able to access another user's tasks.
- **Single Source of Truth:** All project standards and technical choices are governed by this constitution.

## Tech Stack (Phase 2 Standards)
- **Frontend:** Next.js 15+ (App Router), Tailwind CSS, Lucide React Icons.
- **Backend:** Python FastAPI.
- **Database:** Neon Serverless PostgreSQL.
- **Authentication:** Better Auth (with JWT Plugin enabled for cross-platform communication).
- **ORM Tools:**
  - **Frontend:** Drizzle ORM (Required for Better Auth schema and initial DB setup).
  - **Backend:** SQLModel (Required for professional API development and data validation).

## Project Structure & Specs
The project is divided into two major phases/specs:

1. **Spec-1 (Frontend & Auth):**
   - **Initialization:** Create a `frontend/` directory.
   - **Auth Setup:** Integrate Better Auth using MCP (Context-7) documentation. Enable JWT support.
   - **Database Config:** Install `drizzle-orm @neondatabase/serverless` and `drizzle-kit`. Configure schema for Users and Tasks.
   - **UI/UX:** Build a professional dashboard with task management (Add, View, Stats, Update, Delete) using Tailwind CSS.
   - **Integration:** Ensure all API calls include the `Authorization: Bearer <JWT>` header.

2. **Spec-2 (Backend & API):**
   - **Initialization:** Create a `backend/` directory using `uv` for environment management.
   - **API Implementation:** Develop RESTful endpoints (`GET`, `POST`, `PUT`, `DELETE`, `PATCH`) using SQLModel.
   - **Security:** Implement a middleware to verify Better Auth JWT tokens and extract the `user_id` to filter database queries.
```

## Response Summary
Updated the constitution file to reflect Phase 2 requirements, incorporating all specified principles and technical standards for the full-stack todo application.