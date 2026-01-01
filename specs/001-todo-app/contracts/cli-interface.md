# CLI Interface Contract: Todo In-Memory Console Application

**Feature**: 001-todo-app
**Date**: 2026-01-01

## Command Structure

The application follows the pattern: `python todo_app/main.py <command> [arguments]`

## Commands Specification

### ADD Command
- **Syntax**: `add <title> [description]`
- **Parameters**:
  - `title`: Required string (non-empty after trimming)
  - `description`: Optional string
- **Success Response**:
  - Task created with unique ID
  - Confirmation message: "Task #ID created: <title>"
- **Error Responses**:
  - Empty title: "Error: Title cannot be empty"
  - Invalid syntax: "Error: Invalid syntax. Use: add <title> [description]"

### LIST Command
- **Syntax**: `list`
- **Parameters**: None
- **Success Response**:
  - Tabular display of all tasks
  - Columns: ID, Title, Description, Status
  - Completed tasks marked with checkmark (✓)
  - Incomplete tasks marked with empty box (○)
- **Error Responses**: None

### UPDATE Command
- **Syntax**: `update <id> <title> [description]`
- **Parameters**:
  - `id`: Required integer (existing task ID)
  - `title`: Required string (non-empty after trimming)
  - `description`: Optional string
- **Success Response**:
  - Task updated
  - Confirmation message: "Task #ID updated"
- **Error Responses**:
  - Invalid ID: "Error: Task #ID not found"
  - Empty title: "Error: Title cannot be empty"
  - Invalid syntax: "Error: Invalid syntax. Use: update <id> <title> [description]"

### COMPLETE Command
- **Syntax**: `complete <id>`
- **Parameters**:
  - `id`: Required integer (existing task ID)
- **Success Response**:
  - Task marked as complete
  - Confirmation message: "Task #ID marked as complete"
- **Error Responses**:
  - Invalid ID: "Error: Task #ID not found"
  - Invalid syntax: "Error: Invalid syntax. Use: complete <id>"

### INCOMPLETE Command
- **Syntax**: `incomplete <id>`
- **Parameters**:
  - `id`: Required integer (existing task ID)
- **Success Response**:
  - Task marked as incomplete
  - Confirmation message: "Task #ID marked as incomplete"
- **Error Responses**:
  - Invalid ID: "Error: Task #ID not found"
  - Invalid syntax: "Error: Invalid syntax. Use: incomplete <id>"

### DELETE Command
- **Syntax**: `delete <id>`
- **Parameters**:
  - `id`: Required integer (existing task ID)
- **Success Response**:
  - Task removed from list
  - Confirmation message: "Task #ID deleted"
- **Error Responses**:
  - Invalid ID: "Error: Task #ID not found"
  - Invalid syntax: "Error: Invalid syntax. Use: delete <id>"

## Input Validation Rules

1. **ID Validation**: Must be a positive integer that exists in the current task list
2. **Title Validation**: Must be a non-empty string after trimming whitespace
3. **Description Validation**: Can be any string (including empty) or omitted
4. **Command Validation**: Must be one of the supported commands (add, list, update, complete, incomplete, delete)

## Error Handling Contract

All errors follow the format: "Error: [specific message]"
- User input errors provide guidance on correct usage
- Invalid IDs result in "not found" messages
- Syntax errors provide example of correct syntax
- Application never crashes on invalid input

## Exit Codes

- 0: Success
- 1: User input error
- 2: System error