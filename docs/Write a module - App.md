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
            css/
                tasks.css
```

---

### **2. Define the Manifest File**

The manifest file specifies metadata about the module. Create `__manifest__.py` inside the `tasks` directory:

```python
manifest = {
    'name': 'Tasks',
    'version': '1.0',
    'main_route': '/tasks',
    'icon_class': 'fa-regular fa-check-square',
    'type': 'App',
    'color': '#007bff',  # Blue color
    'depends': ['core'],
    'enabled': True,
    'description': 'Task and to-do management',
    'long_description': 'Simple yet powerful task management system. Create, organize, and track tasks with ease. Perfect for personal to-dos or team task management.'
}
```

---

### **3. Define the Model**

In the `models` directory, create a file `task.py` to define the database model for tasks:

```python
from system.db.database import db
from flask import current_app

class Task(db.Model):
    __tablename__ = 'task'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    def __init__(self, name):
        self.name = name

    @classmethod
    def create_sample_data(cls):
        """Initialize sample tasks if table is empty"""
        if not cls.query.first():  # Only create if table is empty
            cls.create("Review project requirements")
            cls.create("Schedule team meeting")
            cls.create("Update documentation")
            print("Sample tasks created")

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

In the `controllers` directory, create a file `routes.py`:

```python
from flask import Blueprint, render_template, request, redirect, url_for, g, flash
from flask_login import login_required
from ..models.task import Task

blueprint = Blueprint(
    'tasks_bp',
    __name__,
    template_folder='../views/templates',
    static_folder='../views/assets'
)

@blueprint.route("/")
@login_required
def tasks_home():
    """Tasks home page"""
    try:
        tasks = Task.get_all()
    except:
        tasks = []  # If table doesn't exist or any other error, just use empty list
        
    return render_template("tasks.html",
                        title=g.current_module['name'],
                        module_name=g.current_module['name'],
                        module_icon=g.current_module['icon_class'],
                        page_icon=g.current_module['icon_class'],
                        icon_color=g.current_module['color'],
                        module_home='tasks_bp.tasks_home',
                        installed_modules=g.installed_modules,
                        tasks=tasks,
                        flash_duration=1000)
```

---

### **5. Create Module Class**

Create `module.py` to handle module initialization:

```python
from system.db.database import db
from flask import current_app
from system.module.hooks import hookimpl

class TasksModule:
    def __init__(self):
        """Initialize module"""
        self._blueprint = None
        self._url_prefix = None

    def register_blueprint(self, blueprint, url_prefix):
        """Register blueprint with the module"""
        self._blueprint = blueprint
        self._url_prefix = url_prefix

    def get_routes(self):
        """Get module routes"""
        from .controllers.routes import blueprint as tasks_blueprint
        return [(tasks_blueprint, '/tasks')]

    @hookimpl
    def init_database(self):
        """Initialize database tables and sample data"""
        from .models.task import Task
        db.create_all()
        try:
            Task.create_sample_data()
        except Exception as e:
            print(f"Error creating sample tasks: {e}")
```

---

### **6. Create Templates**

In `views/templates`, create `tasks.html`:

```html
{% extends "base.html" %}

{% block title %}{{ _("Tasks") }}{% endblock %}

{% block app_class %}tasks-app{% endblock %}

{% block additional_styles %}
<link rel="stylesheet" href="{{ url_for('tasks_bp.static', filename='css/tasks.css') }}">
{% endblock %}

{% block content %}
<div class="content-card tasks-container">
    <div class="tasks-header">
        <h2>{{ _("Tasks") }}</h2>
        <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#addTaskModal">
            <i class="fas fa-plus"></i> {{ _("Add Task") }}
        </button>
    </div>

    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            {% for category, message in messages %}
                <div class="alert alert-{{ category }} alert-dismissible fade show" role="alert" id="flash-{{ loop.index }}">
                    {{ message }}
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
            {% endfor %}
        {% endif %}
    {% endwith %}
</div>
{% endblock %}
```

---

### **7. Add CSS Styling**

In `views/assets/css`, create `tasks.css`:

```css
/* Tasks Module Styles */
.tasks-app {
    --module-color: #dc3545;
    --flash-duration: 3000ms;  /* Configure flash message duration */
}

.tasks-app .app-header {
    border-bottom-color: var(--module-color);
}

.app-icon-tasks,
[data-app="Tasks"] i {
    color: var(--module-color) !important;
}

/* Tasks layout */
.tasks-container {
    max-width: 1000px;
    margin: 0 auto;
    padding: 2rem;
}

.tasks-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
}

.tasks-header h2 {
    margin: 0;
}
```

---

### **8. Add Translations**

Create a `lang` directory in your module with language files:

```
tasks/
    lang/
        es.json
```

Example translation file (es.json):
```json
{
    "_meta": {
        "date_formats": {
            "short": "DD/MM/YYYY",
            "medium": "DD MMM YYYY",
            "long": "DD [de] MMMM [de] YYYY",
            "time": "HH:mm",
            "datetime": "DD/MM/YYYY HH:mm"
        },
        "number_formats": {
            "decimal_separator": ",",
            "thousand_separator": ".",
            "currency_symbol": "€",
            "currency_format": "{symbol}{amount}"
        }
    },
    "Tasks": "Tareas",
    "Add Task": "Agregar Tarea",
    "Edit Task": "Editar Tarea",
    "Delete Task": "Eliminar Tarea"
}
```

---

### **9. Test Your Module**

1. Start the Flask application
2. Visit `/tasks` in your browser
3. Verify that:
   - The module appears in the app selector
   - Tasks page loads with proper styling
   - Translations work when changing language
   - Sample tasks are created in the database

This creates a fully functional Tasks module that integrates with the sparQ platform's core features including authentication, internationalization, and the module system.

