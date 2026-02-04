/**
 * Server-side API Service
 * Handles all communication with the backend API
 * Production-ready with proper error handling and logging
 */

import type { Task, TaskCreateInput, TaskUpdateInput, TaskResponse } from '@/types/task';

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';

/**
 * Create request headers with JWT authentication
 */
function createHeaders(jwt: string): HeadersInit {
  return {
    'Authorization': `Bearer ${jwt}`,
    'Content-Type': 'application/json',
  };
}

/**
 * Handle API errors consistently
 */
async function handleApiError(response: Response, operation: string): Promise<never> {
  const errorText = await response.text().catch(() => 'Unknown error');
  const errorMessage = `${operation} failed: ${response.status} ${response.statusText} - ${errorText}`;
  console.error(errorMessage);
  throw new Error(errorMessage);
}

/**
 * Get all tasks for a user
 */
export async function getUserTasks(userId: string, jwt: string): Promise<Task[]> {
  try {
    const url = `${BACKEND_URL}/api/v1/${userId}/tasks`;

    const response = await fetch(url, {
      headers: createHeaders(jwt),
      cache: 'no-store', // Always fetch fresh data
      next: { revalidate: 0 },
    });

    if (!response.ok) {
      await handleApiError(response, 'Fetch tasks');
    }

    const tasks = await response.json();
    console.log(`✓ Fetched ${tasks.length} tasks for user ${userId}`);
    return tasks;
  } catch (error) {
    console.error('Error fetching tasks:', error);
    // Return empty array to prevent UI crashes
    return [];
  }
}

/**
 * Create a new task
 */
export async function createTask(
  userId: string,
  taskData: TaskCreateInput,
  jwt: string
): Promise<TaskResponse> {
  const url = `${BACKEND_URL}/api/v1/${userId}/tasks`;

  const response = await fetch(url, {
    method: 'POST',
    headers: createHeaders(jwt),
    body: JSON.stringify(taskData),
  });

  if (!response.ok) {
    await handleApiError(response, 'Create task');
  }

  const task = await response.json();
  console.log(`✓ Created task: ${task.id}`);
  return task;
}

/**
 * Update an existing task
 */
export async function updateTask(
  userId: string,
  taskId: string,
  taskData: TaskUpdateInput,
  jwt: string
): Promise<TaskResponse> {
  const url = `${BACKEND_URL}/api/v1/${userId}/tasks/${taskId}`;

  const response = await fetch(url, {
    method: 'PUT',
    headers: createHeaders(jwt),
    body: JSON.stringify(taskData),
  });

  if (!response.ok) {
    await handleApiError(response, 'Update task');
  }

  const task = await response.json();
  console.log(`✓ Updated task: ${taskId}`);
  return task;
}

/**
 * Delete a task
 */
export async function deleteTask(
  userId: string,
  taskId: string,
  jwt: string
): Promise<void> {
  const url = `${BACKEND_URL}/api/v1/${userId}/tasks/${taskId}`;

  const response = await fetch(url, {
    method: 'DELETE',
    headers: createHeaders(jwt),
  });

  if (!response.ok) {
    await handleApiError(response, 'Delete task');
  }

  console.log(`✓ Deleted task: ${taskId}`);
}

/**
 * Toggle task completion status
 */
export async function toggleTaskCompletion(
  userId: string,
  taskId: string,
  completed: boolean,
  jwt: string
): Promise<TaskResponse> {
  const url = `${BACKEND_URL}/api/v1/${userId}/tasks/${taskId}/complete`;

  const response = await fetch(url, {
    method: 'PATCH',
    headers: createHeaders(jwt),
    body: JSON.stringify({ completed }),
  });

  if (!response.ok) {
    await handleApiError(response, 'Toggle task completion');
  }

  const task = await response.json();
  console.log(`✓ Toggled task ${taskId} completion to: ${completed}`);
  return task;
}