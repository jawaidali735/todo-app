# Todo In-Memory Console Application

A simple command-line todo application that stores tasks in memory during runtime. The application provides core task management functionality with clear user feedback and robust error handling.

## Features

- Add tasks with a unique numeric identifier, title, and optional description
- View all tasks with their completion status
- Update existing tasks' title and description
- Mark tasks as complete or incomplete
- Delete tasks using their identifier
- All operations provide clear confirmation or error messages

## Requirements

- Python 3.13 or later

## Installation

No installation required. The application uses only Python standard library.

## Usage

```bash
# Add a task
python todo_app/main.py add "Task title" "Optional description"

# View all tasks
python todo_app/main.py list

# Update a task
python todo_app/main.py update <task_id> "New title" "Optional new description"

# Mark task as complete
python todo_app/main.py complete <task_id>

# Mark task as incomplete
python todo_app/main.py incomplete <task_id>

# Delete a task
python todo_app/main.py delete <task_id>
```

### Examples

```bash
# Add a task
python todo_app/main.py add "Buy groceries" "Milk, bread, eggs"

# View all tasks
python todo_app/main.py list

# Mark task 1 as complete
python todo_app/main.py complete 1

# Update task 1
python todo_app/main.py update 1 "Buy groceries" "Milk, bread, eggs, fruits"

# Delete task 1
python todo_app/main.py delete 1
```

## Memory-Only Storage

All tasks exist only during the application session. When the application terminates, all tasks are lost. This is by design and documented in the application behavior.

## Error Handling

The application provides clear error messages for:
- Invalid command syntax
- Non-existent task IDs
- Empty or invalid titles
- Missing required arguments

## Architecture

The application follows a clear separation of concerns:
- **CLI Interface**: `main.py` handles user input/output and command parsing
- **Business Logic**: `task_manager.py` contains core task management operations
- **Data Model**: `models/task.py` defines task structure
- **Utilities**: `utils/validators.py` contains input validation utilities