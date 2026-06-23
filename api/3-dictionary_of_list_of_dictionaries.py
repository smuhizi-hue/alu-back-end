#!/usr/bin/python3
"""
Script that exports TODO list data for all employees into a single JSON file.
"""
import json
import requests

if __name__ == "__main__":
    # Base URL for the REST API
    url = "https://jsonplaceholder.typicode.com/"
    
    # Fetch all users to create a mapping of userId to username
    users_response = requests.get(f"{url}users").json()
    # Create a dictionary {user_id: username} for quick lookup
    users_dict = {str(user.get("id")): user.get("username") for user in users_response}
    
    # Fetch all tasks from all employees
    todos_response = requests.get(f"{url}todos").json()
    
    # Initialize the final dictionary structure
    all_employees_data = {}
    
    # Initialize an empty list for each user in the final data
    for user_id in users_dict.keys():
        all_employees_data[user_id] = []
        
    # Populate the dictionary with the tasks formatted correctly
    for task in todos_response:
        user_id = str(task.get("userId"))
        # Only process if the user exists in our users dictionary
        if user_id in users_dict:
            all_employees_data[user_id].append({
                "username": users_dict[user_id],
                "task": task.get("title"),
                "completed": task.get("completed")
            })
            
    # Define the output file name
    filename = "todo_all_employees.json"
    
    # Write the compact JSON data into the file
    with open(filename, mode='w', encoding='utf-8') as json_file:
        json.dump(all_employees_data, json_file)
