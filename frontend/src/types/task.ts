// Shared types for Task entity across the application

export interface Task {
  id: string;
  userId: string;
  title: string;
  description?: string;
  completed: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface TaskCreateInput {
  title: string;
  description?: string;
}

export interface TaskUpdateInput {
  title?: string;
  description?: string;
}

export interface TaskCompleteInput {
  completed: boolean;
}

// API Response types
export interface ApiError {
  detail: string;
  status: number;
}

export interface TaskResponse extends Task {}
export interface TaskListResponse extends Array<Task> {}
