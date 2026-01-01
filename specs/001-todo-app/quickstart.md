# Quickstart Guide: Todo In-Memory Console Application

**Feature**: 001-todo-app
**Date**: 2026-01-01

## Prerequisites

- Python 3.13 or later
- Package manager: uv (optional, for dependency management if needed)

## Setup

1. Ensure Python 3.13+ is installed:
   ```bash
   python --version
   ```

2. Clone or access the project directory

3. No additional dependencies needed (using standard library only)

## Running the Application

```bash
python todo_app/main.py
```

## Available Commands

### Add a Task
```bash
python todo_app/main.py add "Task title" "Optional description"
```

### View All Tasks
```bash
python todo_app/main.py list
```

### Update a Task
```bash
python todo_app/main.py update <task_id> "New title" "Optional new description"
```

### Mark Task as Complete
```bash
python todo_app/main.py complete <task_id>
```

### Mark Task as Incomplete
```bash
python todo_app/main.py incomplete <task_id>
```

### Delete a Task
```bash
python todo_app/main.py delete <task_id>
```

## Example Usage

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

## Expected Output Format

Tasks are displayed in a tabular format with columns:
- ID: Sequential number
- Title: Task title
- Description: Optional task description
- Status: "Complete" or "Incomplete"

## Error Handling

The application provides clear error messages for:
- Invalid command syntax
- Non-existent task IDs
- Empty or invalid titles
- Missing required arguments

## Memory-Only Storage Note

All tasks exist only during the application session. When the application terminates, all tasks are lost. This is by design and documented in the application behavior.