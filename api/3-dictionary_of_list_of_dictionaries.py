#!/usr/bin/python3
"""
Script that fetches TODO list progress for all employees from a REST API
and exports the data to JSON format.
"""

import json
import requests
import sys


def get_all_employees_todo_progress():
    """
    Get TODO list progress for all employees and export to JSON.
    """
    # Base URL for the API
    base_url = "https://jsonplaceholder.typicode.com"
    
    try:
        # Fetch all users
        users_response = requests.get(f"{base_url}/users")
        users_response.raise_for_status()
        users = users_response.json()
        
        # Fetch all todos
        todos_response = requests.get(f"{base_url}/todos")
        todos_response.raise_for_status()
        all_todos = todos_response.json()
        
        # Create a dictionary to store all employee tasks
        all_employees_data = {}
        
        # Process each user
        for user in users:
            user_id = user.get('id')
            username = user.get('username')
            
            # Filter todos for this user - ensure we get all tasks
            user_todos = [todo for todo in all_todos if todo.get('userId') == user_id]
            
            # Prepare task list for this user
            task_list = []
            for todo in user_todos:
                task_dict = {
                    "username": username,
                    "task": todo.get('title'),
                    "completed": todo.get('completed')
                }
                task_list.append(task_dict)
            
            # Add to the main dictionary - this ensures ALL users appear
            all_employees_data[str(user_id)] = task_list
            
            # Display progress for this employee
            total_tasks = len(user_todos)
            completed_tasks = [todo for todo in user_todos if todo.get('completed')]
            done_count = len(completed_tasks)
            print(f"Employee {user.get('name')} is done with tasks({done_count}/{total_tasks})")
        
        # Export to JSON
        json_filename = "todo_all_employees.json"
        
        # Write to JSON file
        with open(json_filename, mode='w', encoding='utf-8') as json_file:
            json.dump(all_employees_data, json_file, indent=4)
        
        print(f"\nData exported to {json_filename}")
        print(f"Total employees processed: {len(users)}")
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"Error parsing JSON: {e}")
        sys.exit(1)
    except IOError as e:
        print(f"Error writing to JSON file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    get_all_employees_todo_progress()
