# Data Model: Backend HTTP + DB Upgrade

## Entity: Task

**Description**: Represents a user's task with properties and state

**Fields**:
- `id`: UUID (Primary Key, indexed, auto-generated)
- `user_id`: TEXT/UUID (Foreign Key to user, indexed, required)
- `title`: VARCHAR(200) (Required, maximum 200 characters)
- `description`: TEXT (Optional, unlimited length)
- `completed`: BOOLEAN (Default: false, indicates task completion status)
- `created_at`: TIMESTAMP (Auto-generated, indicates creation time)
- `updated_at`: TIMESTAMP (Auto-generated, updated on any modification)

**Validation Rules**:
- `title` must not be empty or whitespace-only
- `title` length must be ≤ 200 characters
- `user_id` must match authenticated user's ID
- `completed` must be boolean value (true/false)

**State Transitions**:
- `completed = false` → `completed = true` (when task is marked complete)
- `completed = true` → `completed = false` (when task is marked incomplete)

**Relationships**:
- Belongs to one User (via `user_id` foreign key)
- All queries must be filtered by `user_id` for isolation

## Entity: User (Reference)

**Description**: Represents an authenticated user identified by their unique ID from JWT claims

**Fields** (stored in Better Auth, referenced via JWT):
- `user_id`: TEXT/UUID (Subject claim from JWT, used for filtering)
- `email`: TEXT (Email claim from JWT)
- `expires_at`: TIMESTAMP (Expiration claim from JWT)

**Access Control**:
- All Task operations must validate that `user_id` in JWT matches the `user_id` in the request
- No direct User entity manipulation in this service (handled by Better Auth)

## Database Schema

### Table: tasks
```sql
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id TEXT NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_user_completed ON tasks(user_id, completed);
```

### Indexes:
- `idx_tasks_user_id`: Optimizes user-specific queries
- `idx_tasks_user_completed`: Optimizes filtered queries (pending/completed tasks per user)

## API Request/Response Models

### Task Creation Request
```json
{
  "title": "string (required, max 200 chars)",
  "description": "string (optional)"
}
```

### Task Response
```json
{
  "id": "UUID string",
  "user_id": "TEXT string",
  "title": "string",
  "description": "string or null",
  "completed": "boolean",
  "created_at": "ISO 8601 datetime string",
  "updated_at": "ISO 8601 datetime string"
}
```

### Task Update Request
```json
{
  "title": "string (optional, max 200 chars)",
  "description": "string (optional)"
}
```

### Task Completion Toggle Request
```json
{
  "completed": "boolean (required)"
}
```

## Query Patterns

### List User Tasks
- Filter: `WHERE user_id = :authenticated_user_id`
- Optional filters: `AND completed = :status_filter`

### Get Specific Task
- Filter: `WHERE user_id = :authenticated_user_id AND id = :task_id`

### Update/Delete Task
- Filter: `WHERE user_id = :authenticated_user_id AND id = :task_id`
- Verify record exists before operation

## Security Constraints

- All database queries must include `user_id` filter clause
- No queries should return tasks without user_id validation
- User ID in URL path must match JWT user_id claim before any database operation