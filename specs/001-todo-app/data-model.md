# Data Model: Todo In-Memory Console Application

**Feature**: 001-todo-app
**Date**: 2026-01-01

## Task Entity

### Fields
- **id**: `int` - Unique sequential identifier for the task within the session (required, positive integer)
- **title**: `str` - Title of the task (required, non-empty string)
- **description**: `str` - Optional description of the task (optional, can be None or empty)
- **completed**: `bool` - Completion status of the task (required, default: False)

### Validation Rules
- ID must be a positive integer
- Title must be a non-empty string (after trimming whitespace)
- Description can be any string or None
- Completed status must be a boolean value

### State Transitions
- `incomplete` → `complete`: When user marks task as complete
- `complete` → `incomplete`: When user marks task as incomplete

## Task List Collection

### Structure
- **tasks**: `List[Task]` - In-memory collection of all tasks in the current session
- **next_id**: `int` - Counter for generating next unique task ID (starts at 1)

### Operations
- Add task: Append to list, assign next available ID
- Remove task: Remove by ID, maintain ID sequence
- Update task: Modify existing task by ID
- Find task: Retrieve by ID
- List all: Return all tasks in the collection

### Constraints
- All operations maintain in-memory storage only
- No persistence beyond application session
- IDs remain unique within session
- Maximum theoretical capacity limited only by available memory