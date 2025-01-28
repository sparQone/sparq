# How to Create a New Application Module in sparQ

This document will guide you through creating a new module of type **Application** in the sparQ platform. Applications are standalone modules that add new functionality without modifying other modules. In this guide, we will create a simple "Task Manager" application.

---

## **Steps to Create an Application Module**

### **1. Directory Structure**

Each application module resides in the `modules` directory. To create the "Task Manager" application:

1. Navigate to the `modules` directory.
2. Create a new directory named `tasks`.
3. Inside `tasks`, create the following structure:

```
tasks/
    __init__.py
    __manifest__.py
    module.py
    models/
        __init__.py
        task.py
    controllers/
        routes.py
    views/
        templates/
            tasks.html
        assets/
            styles.css
```

---

### **2. Define the Manifest File**

The manifest file specifies metadata about the module. Create `__manifest__.py` inside the `tasks` directory with the following content:

```python
manifest = {
    "name": "TaskManagerModule",
    "type": "Application",
    "description": "A module for managing tasks.",
    "version": "1.0.0"
}
```

---

### **3. Define the Model**

In the `models` directory, create a file `task.py` to define the database model for tasks.

```python
from system.db.database import db

class Task(db.Model):
    __tablename__ = 'task'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __init__(self, name):
        self.name = name

    @staticmethod
    def create(name):
        task = Task(name=name)
        db.session.add(task)
        db.session.commit()
        return task

    @staticmethod
    def get_all():
        return Task.query.all()

    @staticmethod
    def delete(task_id):
        task = Task.query.get(task_id)
        if task:
            db.session.delete(task)
            db.session.commit()

    @staticmethod
    def update(task_id, name):
        task = Task.query.get(task_id)
        if task:
            task.name = name
            db.session.commit()
            return task
        return None
```

---

### **4. Create Controllers and Routes**

In the `controllers` directory, create a file `routes.py` for handling HTTP routes.

```python
from flask import Blueprint, render_template, request, jsonify
from tasks.models.task import Task

tasks_bp = Blueprint('tasks_bp', __name__, template_folder='../views/templates', static_folder='../views/assets')

@tasks_bp.route('/tasks', methods=['GET'])
def index():
    tasks = Task.get_all()
    return render_template('tasks.html', tasks=tasks)

@tasks_bp.route('/tasks', methods=['POST'])
def create_task():
    name = request.form.get('name')
    task = Task.create(name)
    return jsonify({"id": task.id, "name": task.name})

@tasks_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    Task.delete(task_id)
    return jsonify({"status": "success"})

@tasks_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    name = request.form.get('name')
    task = Task.update(task_id, name)
    if task:
        return jsonify({"id": task.id, "name": task.name})
    return jsonify({"error": "Task not found"}), 404
```

---

### **5. Create Templates and CSS**

#### **HTML Template**
In `views/templates`, create a `tasks.html` file for the UI.

```html
<!DOCTYPE html>
<html>
<head>
    <title>Task Manager</title>
    <link rel="stylesheet" type="text/css" href="/assets/styles.css">
</head>
<body>
    <div class="container">
        <h1>Task Manager</h1>
        <form id="task-form">
            <input type="text" name="name" placeholder="New Task" required>
            <button type="submit">Add Task</button>
        </form>
        <ul id="task-list">
            {% for task in tasks %}
            <li data-id="{{ task.id }}">{{ task.name }}</li>
            {% endfor %}
        </ul>
    </div>
    <script>
        document.getElementById('task-form').addEventListener('submit', async function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            const response = await fetch('/tasks', {
                method: 'POST',
                body: formData
            });
            const task = await response.json();
            const li = document.createElement('li');
            li.textContent = task.name;
            li.dataset.id = task.id;
            document.getElementById('task-list').appendChild(li);
        });
    </script>
</body>
</html>
```

#### **CSS File**
In `views/assets`, create a `styles.css` file to style the Task Manager UI.

```css
body {
    font-family: Arial, sans-serif;
    background-color: #f4f4f9;
    color: #333;
    margin: 0;
    padding: 0;
}

.container {
    max-width: 600px;
    margin: 50px auto;
    background: #fff;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

h1 {
    text-align: center;
    color: #555;
}

form {
    display: flex;
    margin-bottom: 20px;
}

form input {
    flex: 1;
    padding: 10px;
    font-size: 16px;
    border: 1px solid #ddd;
    border-radius: 4px;
    margin-right: 10px;
}

form button {
    padding: 10px 20px;
    font-size: 16px;
    background-color: #5cb85c;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

form button:hover {
    background-color: #4cae4c;
}

ul {
    list-style: none;
    padding: 0;
}

ul li {
    padding: 10px;
    background: #f9f9f9;
    border: 1px solid #ddd;
    margin-bottom: 10px;
    border-radius: 4px;
}
```

---

### **6. Register the Module**

In `module.py`, register the blueprint for the module.

```python
from tasks.controllers.routes import tasks_bp

class TaskManagerModule:
    def __init__(self, app):
        app.register_blueprint(tasks_bp)
```

---

### **7. Test Your Module**

1. Start the Flask application.
2. Visit `/tasks` in your browser.
3. Add, update, and delete tasks using the provided UI and verify the functionality.

---

With these steps, you have created a fully functional "Task Manager" module of type **Application**. It demonstrates CRUD operations, dynamic module loading, and a simple UI with CSS styling. This example can serve as a template for other application modules.

