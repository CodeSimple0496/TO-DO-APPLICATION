# Basic Structure

def display_menu():
    print("1. View Tasks")
    print("2. Add Task")
    print("3. Mark Task as Completed")
    print("4. Delete Task")
    print("5. Exit")



def main():
    tasks = []
    while True:
        display_menu()
        choice = input("Choose an option: ")
        
        if choice == '1':
            if not tasks:
                print("No tasks available.")
            else:
                for idx, task in enumerate(tasks, 1):
                    status = "✓" if task['completed'] else "✗"
                    print(f"{idx}. [{status}] {task['description']}")
        
        elif choice == '2':
            description = input("Enter task description: ")
            tasks.append({'description': description, 'completed': False})
            print("Task added.")
        
        elif choice == '3':
            task_num = int(input("Enter task number to mark as completed: ")) - 1
            if 0 <= task_num < len(tasks):
                tasks[task_num]['completed'] = True
                print("Task marked as completed.")
            else:
                print("Invalid task number.")
        
        elif choice == '4':
            task_num = int(input("Enter task number to delete: ")) - 1
            if 0 <= task_num < len(tasks):
                tasks.pop(task_num)
                print("Task deleted.")
            else:
                print("Invalid task number.")
        
        elif choice == '5':
            print("Exiting the program.")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()



## Start with viewing tasks
def view_tasks(tasks):
    if not tasks:
        print("No tasks in your list!")
        return
    
    print("\n--- Your Tasks ---")
    for i, task in enumerate(tasks, 1):
        status = "✓" if task['completed'] else " "
        print(f"{i}. [{status}] {task['description']}")



## Then add task functionality
def add_task(tasks):
    description = input("Enter the task description: ").strip()
    if description:
        task = {
            'description': description,
            'completed': False 
        }
        tasks.append(task)
        print(f"Task '{description}' added!")
    else:
        print("Task description cannot be empty!")


## Add mark compelete function
def mark_complete(tasks):
    view_tasks(tasks)
    if not tasks:
        return
    try:
        task_num = int(input("Enter task number to mark complete: "))
        if 1 <= task_num <= len(tasks):
            tasks[task_num - 1]['completed'] = True
            print(f"Task {task_num} marked as completed!")
        else:
            print("Invalid task number!")
    except ValueError:
        print("Please enter a valid nummber!")



## Add delete function
def delete_task(tasks):
    view_tasks(tasks)
    if not tasks:
        return
    
    try:
        task_num = int(input("Enter task number to delete: "))
        if 1 <= task_num <= len(tasks):
            removed_task = tasks.pop(task_num - 1)
            print(f"Task '{removed_task['description']}' deleted!")
        else:
            print("Invalid task number!")
    except ValueError:
        print("Please enter a valid number!")




## Add File Persistence
# Step 5: Save and Load Tasks

import json

def save_tasks(tasks, filename="tasks.json"):
    try:
        with open(filename, 'w') as f:
            json.dump(tasks, f)
        print("Tasks saved successfully.")
    except Exception as e:
        print(f"Error saving tasks: {e}")


def load_tasks(filename="tasks.json"):
    try:
        with open(filename, 'r') as f:
            tasks = json.load(f)
        print("Tasks loaded successfully!")
        return tasks
    except FileNotFoundError:
        print("No saved tasks found. Starting fresh!")
        return []
    except Exception as e:
        print(f"Error loading tasks: {e}")
        return []
    

# Update main function to use file operations
def main():
    tasks = load_tasks()
    while True:
        display_menu()
        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            view_tasks(tasks)
        elif choice == '2':
            add_task(tasks)
            save_tasks(tasks)
        elif choice == '3':
            mark_complete(tasks)
            save_tasks(tasks)
        elif choice == '4':
            delete_task(tasks)
            save_tasks(tasks)
        elif choice == '5':
            save_tasks(tasks)
            print("Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.")


## Phase 4: Enhancement

# Step 5: Add Due Dates and Priorities
from datetime import datetime

def add_task(tasks):
    description = input("Enter the task description: ").strip()
    if not description:
        print("Task description cannot be empty!")
        return
    
    due_date = input("Enter due date (YYYY-MM-DD) or press Enter for none: ").strip() 
    priority = input("Enter priority (HIgh/Medium/Low) [Medium]:").strip() or "Medium"

    task = {
        'description': description,
        'completed': False,
        'due_date': due_date if due_date else None,
        'priority': priority,
        'created at': datetime.now().isoformat()

    }
    task.append(task)
    print(f"Task '{description}' added!")


def view_tasks(tasks):
    if not tasks:
        print("No tasks in your list!")
        return
    
    print("\n--- Your Tasks ---")
    for i, task in enumerate(tasks, 1):
        status = "✓" if task['completed'] else " "
        due_date = task['due_date'] if task['due_date'] else "No due date"
        priority = task['priority']
        print(f"{i}. [{status}] {task['description']} (Due: {due_date}, Priority: {priority})")
        