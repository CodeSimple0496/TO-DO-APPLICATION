import json
import os
from datetime import datetime

class TodoApp:
    def __init__(self, filename="todos.json"):
        self.filename = filename
        self.todos = []
        self.load_todos()
    
    def load_todos(self):
        """Load todos from a JSON file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as file:
                    self.todos = json.load(file)
                print(f"Loaded {len(self.todos)} todo(s) from {self.filename}")
            except (json.JSONDecodeError, IOError):
                print("Error loading todos. Starting with an empty list.")
                self.todos = []
        else:
            self.todos = []
    
    def save_todos(self):
        """Save todos to a JSON file"""
        try:
            with open(self.filename, 'w') as file:
                json.dump(self.todos, file, indent=2)
            return True
        except IOError:
            print("Error saving todos to file.")
            return False
    
    def create_todo(self):
        """Create a new todo item"""
        print("\n--- Create New Todo ---")
        
        title = input("Enter todo title: ").strip()
        if not title:
            print("Title cannot be empty!")
            return
        
        description = input("Enter todo description (optional): ").strip()
        
        todo = {
            "id": len(self.todos) + 1,
            "title": title,
            "description": description,
            "completed": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.todos.append(todo)
        if self.save_todos():
            print(f"Todo '{title}' created successfully with ID: {todo['id']}")
        else:
            print("Todo created but failed to save to file.")
    
    def read_todos(self, show_all=True, show_completed=False):
        """Display todos"""
        print("\n" + "="*50)
        print("TODO LIST")
        print("="*50)
        
        if not self.todos:
            print("No todos found!")
            return
        
        filtered_todos = []
        for todo in self.todos:
            if show_all or todo['completed'] == show_completed:
                filtered_todos.append(todo)
        
        if not filtered_todos:
            status = "completed" if show_completed else "pending"
            print(f"No {status} todos found!")
            return
        
        for todo in filtered_todos:
            status = "✓" if todo['completed'] else "✗"
            print(f"ID: {todo['id']}")
            print(f"Title: {todo['title']}")
            if todo['description']:
                print(f"Description: {todo['description']}")
            print(f"Status: {status}")
            print(f"Created: {todo['created_at']}")
            print(f"Updated: {todo['updated_at']}")
            print("-" * 30)
    
    def update_todo(self):
        """Update an existing todo"""
        print("\n--- Update Todo ---")
        
        try:
            todo_id = int(input("Enter todo ID to update: "))
        except ValueError:
            print("Invalid ID! Please enter a number.")
            return
        
        todo = self.find_todo_by_id(todo_id)
        if not todo:
            print(f"No todo found with ID: {todo_id}")
            return
        
        print(f"\nCurrent title: {todo['title']}")
        new_title = input("Enter new title (press Enter to keep current): ").strip()
        if new_title:
            todo['title'] = new_title
        
        print(f"Current description: {todo['description']}")
        new_description = input("Enter new description (press Enter to keep current): ").strip()
        if new_description is not None:  # Empty string is valid
            todo['description'] = new_description
        
        print(f"Current status: {'Completed' if todo['completed'] else 'Pending'}")
        status_input = input("Mark as completed? (y/n, press Enter to keep current): ").strip().lower()
        if status_input == 'y':
            todo['completed'] = True
        elif status_input == 'n':
            todo['completed'] = False
        
        todo['updated_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if self.save_todos():
            print(f"Todo ID {todo_id} updated successfully!")
        else:
            print("Todo updated but failed to save to file.")
    
    def delete_todo(self):
        """Delete a todo"""
        print("\n--- Delete Todo ---")
        
        try:
            todo_id = int(input("Enter todo ID to delete: "))
        except ValueError:
            print("Invalid ID! Please enter a number.")
            return
        
        todo = self.find_todo_by_id(todo_id)
        if not todo:
            print(f"No todo found with ID: {todo_id}")
            return
        
        confirm = input(f"Are you sure you want to delete '{todo['title']}'? (y/n): ").strip().lower()
        if confirm == 'y':
            self.todos = [t for t in self.todos if t['id'] != todo_id]
            # Reassign IDs to maintain sequence
            for i, t in enumerate(self.todos, 1):
                t['id'] = i
            
            if self.save_todos():
                print(f"Todo ID {todo_id} deleted successfully!")
            else:
                print("Todo deleted but failed to save to file.")
        else:
            print("Deletion cancelled.")
    
    def find_todo_by_id(self, todo_id):
        """Find a todo by ID"""
        for todo in self.todos:
            if todo['id'] == todo_id:
                return todo
        return None
    
    def mark_complete(self):
        """Mark a todo as complete"""
        print("\n--- Mark Todo Complete ---")
        
        try:
            todo_id = int(input("Enter todo ID to mark as complete: "))
        except ValueError:
            print("Invalid ID! Please enter a number.")
            return
        
        todo = self.find_todo_by_id(todo_id)
        if not todo:
            print(f"No todo found with ID: {todo_id}")
            return
        
        todo['completed'] = True
        todo['updated_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if self.save_todos():
            print(f"Todo ID {todo_id} marked as complete!")
        else:
            print("Todo updated but failed to save to file.")
    
    def show_stats(self):
        """Display todo statistics"""
        print("\n--- Todo Statistics ---")
        
        total = len(self.todos)
        completed = sum(1 for todo in self.todos if todo['completed'])
        pending = total - completed
        
        print(f"Total todos: {total}")
        print(f"Completed: {completed}")
        print(f"Pending: {pending}")
        
        if total > 0:
            completion_rate = (completed / total) * 100
            print(f"Completion rate: {completion_rate:.1f}%")
    
    def run(self):
        """Main application loop"""
        print("="*50)
        print("SIMPLE TODO APPLICATION")
        print("="*50)
        
        while True:
            print("\nMenu:")
            print("1. View all todos")
            print("2. View pending todos")
            print("3. View completed todos")
            print("4. Create new todo")
            print("5. Update todo")
            print("6. Delete todo")
            print("7. Mark todo as complete")
            print("8. Show statistics")
            print("9. Save and exit")
            print("0. Exit without saving")
            
            choice = input("\nEnter your choice (0-9): ").strip()
            
            if choice == '1':
                self.read_todos(show_all=True)
            elif choice == '2':
                self.read_todos(show_all=False, show_completed=False)
            elif choice == '3':
                self.read_todos(show_all=False, show_completed=True)
            elif choice == '4':
                self.create_todo()
            elif choice == '5':
                self.update_todo()
            elif choice == '6':
                self.delete_todo()
            elif choice == '7':
                self.mark_complete()
            elif choice == '8':
                self.show_stats()
            elif choice == '9':
                if self.save_todos():
                    print("Todos saved successfully!")
                print("Goodbye!")
                break
            elif choice == '0':
                print("Exiting without saving. Goodbye!")
                break
            else:
                print("Invalid choice! Please enter a number between 0 and 9.")

if __name__ == "__main__":
    app = TodoApp()
    app.run()