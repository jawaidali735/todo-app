'use client';
import { useRef } from 'react';
import { useRouter } from 'next/navigation';
import { useFormStatus } from 'react-dom';
import { addTaskAction } from '@/app/actions/task-actions';

// Sub-component for the submit button that can access form status
function SubmitButton() {
  const { pending } = useFormStatus();
  return (
    <button
      type="submit"
      disabled={pending}
      className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
    >
      {pending ? 'Adding...' : 'Add Task'}
    </button>
  );
}

interface AddTaskFormProps {
  userId: string;
  onTaskAdded?: (task: any) => void;
}

export default function AddTaskForm({ userId, onTaskAdded }: AddTaskFormProps) {
  const formRef = useRef<HTMLFormElement>(null);
  const router = useRouter();

  async function handleSubmit(formData: FormData) {
    try {
      await addTaskAction(formData);
      formRef.current?.reset();
      // Force router refresh to show new task immediately
      router.refresh();
    } catch (error) {
      console.error('Failed to add task:', error);
    }
  }

  return (
    <div className="mb-6">
      <form ref={formRef} action={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
            Task Title
          </label>
          <input
            id="title"
            name="title"
            type="text"
            placeholder="What needs to be done?"
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            required
          />
        </div>
        <div>
          <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
            Description (Optional)
          </label>
          <textarea
            id="description"
            name="description"
            placeholder="Add details..."
            rows={3}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
          />
        </div>
        <SubmitButton />
      </form>
    </div>
  );
}

// Wrapper function for the server action to work with useFormState
async function addTaskActionWithState(prevState: any, formData: FormData) {
  try {
    const title = formData.get('title') as string;

    if (!title.trim()) {
      return {
        ...prevState,
        error: 'Task title is required',
      };
    }

    // Call the original server action
    await addTaskAction(formData);

    // Reset form on success
    if (typeof document !== 'undefined') {
      const form = document.querySelector('form');
      if (form) {
        form.reset();
      }
    }

    return {
      message: 'Task added successfully!',
      error: null,
    };
  } catch (error) {
    return {
      message: '',
      error: error instanceof Error ? error.message : 'Failed to add task. Please try again.',
    };
  }
}