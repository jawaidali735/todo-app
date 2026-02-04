'use server';

import { auth } from '@/lib/auth';
import { headers } from 'next/headers';
import { getJWT } from '@/lib/get-jwt';
import { createTask as createServerTask, updateTask, deleteTask, toggleTaskCompletion } from '@/services/server-api';
import { revalidatePath } from 'next/cache';

export async function addTaskAction(formData: FormData) {
  try {
    const session = await auth.api.getSession({
      headers: await headers()
    });

    if (!session?.user) {
      throw new Error('Unauthorized');
    }

    const jwt = await getJWT();
    if (!jwt) {
      throw new Error('No JWT token');
    }

    const title = formData.get('title') as string;
    const description = formData.get('description') as string;

    await createServerTask(session.user.id, { title, description }, jwt);
    revalidatePath('/dashboard');
  } catch (error) {
    console.error('Error adding task:', error);
    throw error;
  }
}

export async function updateTaskAction(userId: string, taskId: string, taskData: any) {
  try {
    const session = await auth.api.getSession({
      headers: await headers()
    });

    if (!session?.user || session.user.id !== userId) {
      throw new Error('Unauthorized');
    }

    const jwt = await getJWT();
    if (!jwt) {
      throw new Error('No JWT token');
    }

    await updateTask(userId, taskId, taskData, jwt);
    revalidatePath('/dashboard');
  } catch (error) {
    console.error('Error updating task:', error);
    throw error;
  }
}

export async function deleteTaskAction(userId: string, taskId: string) {
  try {
    const session = await auth.api.getSession({
      headers: await headers()
    });

    if (!session?.user || session.user.id !== userId) {
      throw new Error('Unauthorized');
    }

    const jwt = await getJWT();
    if (!jwt) {
      throw new Error('No JWT token');
    }

    await deleteTask(userId, taskId, jwt);
    revalidatePath('/dashboard');
  } catch (error) {
    console.error('Error deleting task:', error);
    throw error;
  }
}

export async function toggleTaskCompletionAction(userId: string, taskId: string, completed: boolean) {
  try {
    const session = await auth.api.getSession({
      headers: await headers()
    });

    if (!session?.user || session.user.id !== userId) {
      throw new Error('Unauthorized');
    }

    const jwt = await getJWT();
    if (!jwt) {
      throw new Error('No JWT token');
    }

    await toggleTaskCompletion(userId, taskId, completed, jwt);
    revalidatePath('/dashboard');
  } catch (error) {
    console.error('Error toggling task completion:', error);
    throw error;
  }
}