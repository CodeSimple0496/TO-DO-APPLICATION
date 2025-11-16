from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Data file
DATA_FILE = 'tasks.json'

def load_tasks():
    """Load tasks from JSON file"""
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        return []
    except Exception as e:
        print(f"Error loading tasks: {e}")
        return []
    
def save_tasks(tasks):
    """Save tasks to JSON file"""
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(tasks, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving tasks: {e}")
        return False
    
@app.route('/')
def home():
    return jsonify({"message": "Todo API is running!"})

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks"""
    tasks = load_tasks()
    return jsonify(tasks)

@app.route('/api/tasks', methods=['POST'])
def add_task():
    """Add a new task"""
    tasks = load_tasks()

    data = request.json
    new_task = {
        'id': len(tasks) + 1,
        'description': data['description'],
        'completed': False,
        'due_data': data.get('due_data'),
        'priority': data.get('priority', 'Medium'),
        'created_at': datetime.now().isoformat()
    }

    tasks.append(new_task)
    save_tasks(tasks)
    return jsonify(new_task), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update a task"""
    tasks = load_tasks()

    for task in tasks:
        if task['id'] == task_id:
            data = request.json
            if 'description' in data:
                task['description'] = data['description']
            if 'completed' in data:
                task['completed'] = data['completed']
            if 'due_date' in data:
                task['due_date'] = data['due_date']
            if 'priority' in data:
                task['priority'] = data['priority']

            save_tasks(tasks)
            return jsonify(task)
    
    return jsonify({"error": "Task not found"}), 404

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task"""
    tasks = load_tasks()
    tasks = [task for task in tasks if task['id'] != task_id]
    save_tasks(tasks)
    return jsonify({"message": "Task deleted"})

@app.route('/api/tasks/<int:task_id>/toggle', methods=['PUT'])
def toggle_task(task_id):
    """Toggle task completion"""
    tasks = load_tasks()

    for task in tasks:
        if task['id'] == task_id:
            task['completed'] = not task['completed']
            save_tasks(tasks)
            return jsonify(task)
        
    return jsonify({"error": "Task not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)