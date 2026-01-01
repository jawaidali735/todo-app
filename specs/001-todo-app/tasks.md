---
description: "Task list for Todo In-Memory Console Application implementation"
---

# Tasks: Todo In-Memory Console Application

**Input**: Design documents from `/specs/001-todo-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `todo_app/` at repository root
- **CLI Application**: `todo_app/main.py`, `todo_app/task_manager.py`, `todo_app/models/task.py`, etc.
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure per implementation plan in todo_app/
- [x] T002 [P] Create main.py entry point for CLI application
- [x] T003 [P] Create task_manager.py for core business logic
- [x] T004 [P] Create models/ directory and task.py for data model

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 Implement Task data model in todo_app/models/task.py with id, title, description, completed fields
- [x] T006 [P] Implement TaskManager class in todo_app/task_manager.py with in-memory storage
- [x] T007 [P] Implement ID generation strategy in TaskManager (sequential integers starting from 1)
- [x] T008 Create CLI argument parsing in todo_app/main.py
- [x] T009 Implement basic error handling and validation utilities
- [x] T010 [P] Create command routing between CLI and TaskManager

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add Tasks (Priority: P1) 🎯 MVP

**Goal**: Allow users to create tasks with a unique numeric identifier, title, and optional description

**Independent Test**: Can be fully tested by running the application and executing the add task command with a title and optional description, and verifying that the task appears in the task list.

### Implementation for User Story 1

- [x] T011 [P] [US1] Implement add_task method in TaskManager class with validation
- [x] T012 [US1] Implement add command in main.py CLI interface
- [x] T013 [US1] Add input validation for add command (title cannot be empty)
- [x] T014 [US1] Implement unique ID assignment for new tasks
- [x] T015 [US1] Add success confirmation message for task creation

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View Task List (Priority: P1)

**Goal**: Allow users to view all tasks with their completion status in the console

**Independent Test**: Can be fully tested by creating one or more tasks and then running the view command to see the list with completion status.

### Implementation for User Story 2

- [x] T016 [P] [US2] Implement list_tasks method in TaskManager class
- [x] T017 [US2] Implement list command in main.py CLI interface
- [x] T018 [US2] Format task display with ID, title, description, and completion status
- [x] T019 [US2] Differentiate completed vs incomplete tasks in display
- [x] T020 [US2] Ensure list command works with empty task list

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Update Tasks (Priority: P2)

**Goal**: Allow users to update existing tasks' title and description using their numeric identifier

**Independent Test**: Can be fully tested by creating a task, then updating its title or description using the update command, and verifying the changes are reflected.

### Implementation for User Story 3

- [x] T021 [P] [US3] Implement update_task method in TaskManager class with validation
- [x] T022 [US3] Implement update command in main.py CLI interface
- [x] T023 [US3] Add input validation for update command (task exists, title not empty)
- [x] T024 [US3] Update task title and description based on ID
- [x] T025 [US3] Add success confirmation message for task updates

---

## Phase 6: User Story 4 - Mark Tasks Complete/Incomplete (Priority: P2)

**Goal**: Allow users to mark tasks as complete or incomplete using their numeric identifier

**Independent Test**: Can be fully tested by creating a task, marking it as complete, then marking it as incomplete again, and verifying the status changes.

### Implementation for User Story 4

- [x] T026 [P] [US4] Implement mark_complete method in TaskManager class
- [x] T027 [P] [US4] Implement mark_incomplete method in TaskManager class
- [x] T028 [US4] Implement complete command in main.py CLI interface
- [x] T029 [US4] Implement incomplete command in main.py CLI interface
- [x] T030 [US4] Add validation to ensure task exists before marking complete/incomplete
- [x] T031 [US4] Add success confirmation messages for status changes

---

## Phase 7: User Story 5 - Delete Tasks (Priority: P2)

**Goal**: Allow users to delete tasks using their numeric identifier

**Independent Test**: Can be fully tested by creating a task, then deleting it, and verifying that it no longer appears in the task list.

### Implementation for User Story 5

- [x] T032 [P] [US5] Implement delete_task method in TaskManager class
- [x] T033 [US5] Implement delete command in main.py CLI interface
- [x] T034 [US5] Add validation to ensure task exists before deletion
- [x] T035 [US5] Add success confirmation message for task deletion
- [x] T036 [US5] Handle error case when attempting to delete non-existent task

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T037 [P] Add comprehensive error handling for all user inputs
- [x] T038 [P] Improve error messages to be more user-friendly
- [x] T039 [P] Add input validation across all commands
- [x] T040 [P] Add help text and usage instructions to CLI
- [x] T041 [P] Add documentation in README.md for the application
- [x] T042 [P] Run quickstart.md validation to ensure all commands work as expected
- [x] T043 [P] Add graceful shutdown handling

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 5 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories

### Within Each User Story

- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all implementation tasks for User Story 1 together:
Task: "Implement add_task method in TaskManager class with validation"
Task: "Implement add command in main.py CLI interface"
Task: "Add input validation for add command (title cannot be empty)"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
   - Developer E: User Story 5
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence