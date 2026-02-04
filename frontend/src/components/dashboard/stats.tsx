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

interface StatsProps {
  tasks: Task[];
}

export default function Stats({ tasks }: StatsProps) {
  const totalTasks = tasks.length;
  const completedTasks = tasks.filter(task => task.completed).length;
  const pendingTasks = totalTasks - completedTasks;

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
      <div className="bg-blue-50 p-4 rounded-lg text-center">
        <h3 className="text-2xl font-bold text-blue-700">{totalTasks}</h3>
        <p className="text-gray-600">Total Tasks</p>
      </div>
      <div className="bg-green-50 p-4 rounded-lg text-center">
        <h3 className="text-2xl font-bold text-green-700">{completedTasks}</h3>
        <p className="text-gray-600">Completed</p>
      </div>
      <div className="bg-yellow-50 p-4 rounded-lg text-center">
        <h3 className="text-2xl font-bold text-yellow-700">{pendingTasks}</h3>
        <p className="text-gray-600">Pending</p>
      </div>
    </div>
  );
}