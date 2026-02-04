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

interface TaskItemProps {
  task: Task;
}

export default function TaskItem({ task }: TaskItemProps) {
  return (
    <div className={`flex items-center justify-between p-3 bg-white rounded border ${task.completed ? 'bg-green-50' : ''}`}>
      <div className="flex items-center">
        <input
          type="checkbox"
          checked={task.completed}
          // onChange would trigger update API call in real app
          className="h-4 w-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500"
        />
        <span className={`ml-3 ${task.completed ? "line-through text-gray-500" : "text-gray-900"}`}>
          {task.title}
        </span>
      </div>
      <span className={`px-2 py-1 text-xs rounded-full ${
        task.completed ? "bg-green-100 text-green-800" : "bg-yellow-100 text-yellow-800"
      }`}>
        {task.completed ? "Completed" : "Pending"}
      </span>
    </div>
  );
}