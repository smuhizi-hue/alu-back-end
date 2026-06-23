#!/usr/bin/python3
"""
Script that fetches TODO list progress for a given employee ID from a REST API
and exports the data to CSV format.
"""

import requests
import sys
import csv


def get_employee_todo_progress(employee_id):
    """
    Get and display TODO list progress for a given employee ID,
    then export to CSV.
    
    Args:
        employee_id (int): The employee ID to fetch TODO list for
    """
    # Base URL for the API
    base_url = "https://jsonplaceholder.typicode.com"
    
    try:
        # Fetch employee details
        user_response = requests.get(f"{base_url}/users/{employee_id}")
        user_response.raise_for_status()
        employee_data = user_response.json()
        employee_name = employee_data.get('name')
        employee_username = employee_data.get('username')
        
        # Fetch TODO list for the employee
        todos_response = requests.get(f"{base_url}/todos", params={"userId": employee_id})
        todos_response.raise_for_status()
        todos = todos_response.json()
        
        # Calculate statistics
        total_tasks = len(todos)
        completed_tasks = [todo for todo in todos if todo.get('completed')]
        done_count = len(completed_tasks)
        
        # Display the progress
        print(f"Employee {employee_name} is done with tasks({done_count}/{total_tasks}):")
        
        # Display completed task titles
        for task in completed_tasks:
            print(f"\t {task.get('title')}")
        
        # Export to CSV
        csv_filename = f"{employee_id}.csv"
        with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
            
            for task in todos:
                csv_writer.writerow([
                    employee_id,
                    employee_username,
                    str(task.get('completed')),
                    task.get('title')
                ])
        
        print(f"\nData exported to {csv_filename}")
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"Error parsing JSON: {e}")
        sys.exit(1)
    except IOError as e:
        print(f"Error writing to CSV file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <employee_id>")
        print("Example: python3 script.py 1")
        sys.exit(1)
    
    try:
        employee_id = int(sys.argv[1])
        if employee_id < 1:
            print("Employee ID must be a positive integer")
            sys.exit(1)
        get_employee_todo_progress(employee_id)
    except ValueError:
        print("Employee ID must be an integer")
        sys.exit(1)
