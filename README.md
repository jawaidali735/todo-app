# Full-Stack Todo Application

A comprehensive full-stack todo application built with modern technologies, featuring user authentication, real-time task management, and persistent storage.

## 🚀 Project Overview

This project was developed in **three distinct phases** to progressively enhance functionality:

- **Phase 1**: Basic in-memory console application
- **Phase 2**: Frontend with authentication and database integration
- **Phase 3**: Full-stack application with HTTP APIs and PostgreSQL persistence

---

## 📊 Phase-Wise Development

### **Phase 1: Todo In-Memory Console Application** (`001-todo-app`)
- **Duration**: Initial development phase
- **Technology Stack**: Python 3.13, uv package manager
- **Features Implemented**:
  - Add tasks with unique identifiers, titles, and descriptions
  - View all tasks with completion status
  - Update existing tasks
  - Mark tasks as complete/incomplete
  - Delete tasks
  - Memory-only storage (session-based)
  - Robust error handling and validation
- **Architecture**:
  - CLI Interface: `main.py` handles user interaction
  - Business Logic: `task_manager.py` manages operations
  - Data Models: `models/task.py` defines structures
  - Utilities: `utils/validators.py` for input validation

### **Phase 2: Full-Stack Enhancement** (`002-frontend-auth-setup` & `003-backend-http-db`)
- **Duration**: Second development phase (consisting of two sub-phases)
- **Sub-Phase 2A** (`002-frontend-auth-setup`):
  - **Technology Stack**: Next.js 16+, Better Auth, Drizzle ORM, Neon Database
  - **Features Implemented**:
    - Modern web interface with Next.js 16+ App Router
    - User authentication system with Better Auth
    - JWT token generation for backend authorization
    - Database integration with Neon (PostgreSQL)
    - Drizzle ORM for database operations
    - Login and signup functionality
    - Dashboard for task management
  - **Key Components**:
    - Frontend authentication with JWT tokens
    - Database schema for user and task management
    - Secure token handling and validation
    - Responsive web interface

- **Sub-Phase 2B** (`003-backend-http-db`):
  - **Technology Stack**: FastAPI, PostgreSQL, JWT Middleware
  - **Features Implemented**:
    - HTTP REST APIs for task management
    - JWT-based authentication and authorization
    - User isolation (each user sees only their tasks)
    - Persistent data storage in PostgreSQL
    - Complete CRUD operations via HTTP endpoints
    - Integration with frontend authentication system
    - Comprehensive unit and integration tests
  - **API Endpoints**:
    - Task creation, retrieval, update, and deletion
    - User-specific task filtering
    - Proper HTTP status codes and JSON responses
    - JWT validation middleware

---

## 🏗️ Final Architecture

The complete application consists of:

### **Frontend** (`frontend/`)
- Next.js 16+ application with App Router
- User authentication and authorization
- Task management dashboard
- Responsive UI components
- JWT token management

### **Backend** (`backend/`)
- FastAPI HTTP services
- JWT authentication middleware
- PostgreSQL database integration
- User isolation and task persistence
- REST API endpoints

### **Database**
- Neon PostgreSQL database
- Drizzle ORM schema management
- Secure data storage and retrieval

---

## 🛠️ Technology Stack

- **Frontend**: Next.js 16+, React 19
- **Authentication**: Better Auth with JWT
- **Backend**: FastAPI, Python 3.13
- **Database**: PostgreSQL (Neon)
- **ORM**: Drizzle ORM
- **Package Manager**: uv, npm
- **Deployment**: Vercel (Frontend)

---

## 🚀 Usage

### **Frontend Setup**
```bash
cd frontend
npm install
npm run dev
```

### **Backend Setup**
```bash
cd backend
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
python -m app.main
```

### **Environment Variables**
Configure the following in your `.env` files:
- `DATABASE_URL`: PostgreSQL connection string
- `BETTER_AUTH_SECRET`: Secret for JWT signing
- `NEXT_PUBLIC_BETTER_AUTH_URL`: Frontend auth URL

---

## 🧪 Testing

The application includes comprehensive tests:
- Unit tests for backend business logic
- Integration tests for API endpoints
- Authentication and authorization validation
- User isolation verification

---

## 🌐 Deployment

- **Frontend**: Deployed on Vercel
- **Backend**: Deployable as FastAPI application
- **Database**: Neon PostgreSQL hosting

---

## 📈 Key Achievements

1. **Progressive Enhancement**: Started with simple console app and evolved to full-stack application
2. **Security**: Implemented JWT-based authentication with user isolation
3. **Scalability**: Database-backed persistence instead of memory-only storage
4. **Modern Tech Stack**: Latest versions of Next.js, FastAPI, and supporting libraries
5. **Clean Architecture**: Separation of concerns between frontend, backend, and database layers