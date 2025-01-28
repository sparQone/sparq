from flask import Blueprint, render_template, request, redirect, url_for, g, flash
from flask_login import login_required
from ..models.task import Task

blueprint = Blueprint(
    'tasks_bp',
    __name__,
    template_folder='../views/templates',
    static_folder='../views/assets'
)

# Tasks home page
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

# Add task
@blueprint.route('/add', methods=['POST'])
@login_required
def add_task():
    name = request.form.get('name')
    if name:
        Task.create(name)
        flash('Task added successfully', 'success')
    return redirect(url_for('tasks_bp.tasks_home'))

# Delete task
@blueprint.route('/delete/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    Task.delete(task_id)
    flash('Task deleted successfully', 'success')
    return redirect(url_for('tasks_bp.tasks_home'))

# Update task
@blueprint.route('/update/<int:task_id>', methods=['POST'])
@login_required
def update_task(task_id):
    name = request.form.get('name')
    if name:
        Task.update(task_id, name)
        flash('Task updated successfully', 'success')
    return redirect(url_for('tasks_bp.tasks_home'))