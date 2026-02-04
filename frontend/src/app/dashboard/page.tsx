/**
 * Dashboard Page - Server Component
 * Displays user tasks with real-time updates
 * Production-ready with proper authentication and error handling
 */

import { auth } from '@/lib/auth';
import { headers } from 'next/headers';
import { redirect } from 'next/navigation';
import AddTaskForm from '@/components/dashboard/add-task-form';
import ClientTaskList from '@/components/dashboard/client-task-list';
import { getJWT } from '@/lib/get-jwt';
import { getUserTasks } from '@/services/server-api';
import SignOutButton from '@/components/SignOutButton';
import type { Task } from '@/types/task';

// Force dynamic rendering - no caching for real-time updates
export const dynamic = 'force-dynamic';
export const revalidate = 0;

export default async function DashboardPage() {
  // 1️⃣ Verify user is authenticated using Better Auth server-side session
  const session = await auth.api.getSession({
    headers: await headers()
  });

  if (!session?.user) redirect('/login');

  // 3️⃣ Fetch tasks from backend ONLY
  // ✅ Do NOT send session.user.id
  // Extract user ID from session to pass to API
  const userId = session.user.id;
  const jwt = await getJWT();
  if (!jwt) redirect('/login'); // no JWT, force login

  let tasks: Task[] = [];
  try {
    tasks = await getUserTasks(userId, jwt);
  } catch (error) {
    console.error('Failed to fetch tasks:', error);
    // Continue with empty tasks array
    tasks = [];
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8 flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
            <p>Welcome, {session.user.name}!</p>
          </div>
          <div>
            <SignOutButton />
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main>
        <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          <div className="px-4 py-6 sm:px-0">

            {/* Task Summary */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
              <div className="bg-blue-50 p-4 rounded-lg text-center">
                <h3 className="text-2xl font-bold text-blue-700">{tasks.length}</h3>
                <p className="text-gray-600">Total Tasks</p>
              </div>
              <div className="bg-green-50 p-4 rounded-lg text-center">
                <h3 className="text-2xl font-bold text-green-700">{tasks.filter((t: Task) => t.completed).length}</h3>
                <p className="text-gray-600">Completed</p>
              </div>
              <div className="bg-yellow-50 p-4 rounded-lg text-center">
                <h3 className="text-2xl font-bold text-yellow-700">{tasks.filter((t: Task) => !t.completed).length}</h3>
                <p className="text-gray-600">Pending</p>
              </div>
            </div>

            {/* Add Task Form */}
            <div className="bg-white shadow rounded-lg p-6 mb-6">
              <AddTaskForm userId={userId} /> {/* Pass user ID */}
            </div>

            {/* Task List */}
            <div className="bg-white shadow rounded-lg p-6">
              <h2 className="text-xl font-semibold mb-4">Your Tasks</h2>
              <ClientTaskList initialTasks={tasks} userId={userId} /> {/* Pass user ID */}
            </div>

          </div>
        </div>
      </main>
    </div>
  );
}
