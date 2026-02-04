'use client';
import { useState, useEffect } from 'react';
import TaskItem from './task-item';

// Define the Task type locally since it's not exported from schema
interface Task {
  id: string;
  userId: string;
  title: string;
  description?: string;
  completed: boolean;
  createdAt: string;
  updatedAt: string;
}

interface TaskListProps {
  initialTasks?: Task[];
}

export default function TaskList({ initialTasks = [] }: TaskListProps) {
  const [tasks, setTasks] = useState<Task[]>(initialTasks);

  // In a real app, you'd fetch tasks from an API
  useEffect(() => {
    // Placeholder for fetching tasks
    // const fetchTasks = async () => {
    //   try {
    //     const response = await fetch('/api/tasks');
    //     const data = await response.json();
    //     setTasks(data);
    //   } catch (error) {
    //     console.error('Failed to fetch tasks:', error);
    //   }
    // };
    // fetchTasks();
  }, []);

  return (
    <div className="space-y-2">
      {tasks.length === 0 ? (
        <div className="text-center py-8 text-gray-500">
          <p>No tasks yet. Create your first task!</p>
        </div>
      ) : (
        tasks.map(task => (
          <TaskItem key={task.id} task={task} />
        ))
      )}
    </div>
  );
}