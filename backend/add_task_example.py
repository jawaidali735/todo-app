import requests
import json

# The server is running on localhost:8000
base_url = "http://localhost:8000"

# Example of how to make a request to add a task
# NOTE: You need to get a real JWT token from your Better Auth system
# For now, I'll show you the exact format, but you'll need to replace 'YOUR_JWT_TOKEN' with a real token

user_id = "your-actual-user-id"  # This should match the user ID from your Better Auth
headers = {
    "Authorization": "Bearer YOUR_JWT_TOKEN",  # Replace with actual token from Better Auth
    "Content-Type": "application/json"
}

# Example task data to add
task_data = {
    "title": "Sample Task from API",
    "description": "This is a sample task created via the API endpoint"
}

print("To add a task to your database, you need to:")
print("1. Get a valid JWT token from your Better Auth system")
print("2. Use the user ID that matches the token")
print("3. Make a POST request like this:")

print(f"\nPOST {base_url}/api/v1/{user_id}/tasks")
print(f"Headers: {headers}")
print(f"Body: {json.dumps(task_data, indent=2)}")

# Example of what the request would look like with a real token:
print("\nExample code for your frontend (after getting JWT from Better Auth):")
example_code = '''
// After user is authenticated with Better Auth
const token = // get from Better Auth (e.g., useAuth hook)
const userId = // get user ID from the token payload or user object

const taskData = {
    title: "My New Task",
    description: "Task description here"
};

fetch('http://localhost:8000/api/v1/' + userId + '/tasks', {
    method: 'POST',
    headers: {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json',
    },
    body: JSON.stringify(taskData)
})
.then(response => response.json())
.then(data => console.log('Task created:', data))
.catch(error => console.error('Error:', error));
'''

print(example_code)

print("\nYour Neon database is ready to receive these requests!")
print("The tasks table has been created and is waiting for data.")