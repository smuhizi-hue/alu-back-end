#!/usr/bin/python3
import requests
import sys

def get_employee_todo_progress(employee_id):
    # Base URL for the REST API
    base_url = "https://jsonplaceholder.typicode.com"
    
    # Fetch user information to get the EMPLOYEE_NAME
    user_res = requests.get(f"{base_url}/users/{employee_id}")
    user_data = user_res.json()
    employee_name = user_data.get("name")
    
    # Fetch todo list for the given employee ID
    todos_res = requests.get(f"{base_url}/todos?userId={employee_id}")
    todos = todos_res.json()
    
    # Calculate task statistics
    total_tasks = len(todos)
    done_tasks = [task for task in todos if task.get("completed") is True]
    number_of_done_tasks = len(done_tasks)
    
    # Format and print the output
    # First line: Employee EMPLOYEE_NAME is done with tasks(NUMBER_OF_DONE_TASKS/TOTAL_NUMBER_OF_TASKS):
    print(f"Employee {employee_name} is done with tasks({number_of_done_tasks}/{total_tasks}):")
    
    # Subsequent lines: Tabulated list of completed task titles
    for task in done_tasks:
        print(f"\t {task.get('title')}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            emp_id = int(sys.argv[1])
            get_employee_todo_progress(emp_id)
        except ValueError:
            print("Please provide a valid integer for the employee ID.")

