# -----------------------------------------------------------------------------
# sparQ
#
# Description:
#     Tasks module routes and controllers for the tasks functionality.
#     Handles the main route and rendering of the tasks home page.
#
# Copyright (c) 2025 remarQable LLC
#
# This software is released under an open-source license.
# See the LICENSE file for details.
# -----------------------------------------------------------------------------

from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import login_required

from ..models.task import Task

# Create blueprint
blueprint = Blueprint(
    "tasks_bp", __name__, template_folder="../views/templates", static_folder="../views/assets"
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

    return render_template(
        "tasks/index.html",
        title="Tasks",
        module_home="tasks_bp.tasks_home",
        tasks=tasks,
        flash_duration=1000,
    )


# Add task
@blueprint.route("/add", methods=["POST"])
@login_required
def add_task():
    name = request.form.get("name")
    if name:
        Task.create(name)
        flash("Task added successfully", "success")
    return redirect(url_for("tasks_bp.tasks_home"))


# Delete task
@blueprint.route("/delete/<int:task_id>", methods=["POST"])
@login_required
def delete_task(task_id):
    Task.delete(task_id)
    flash("Task deleted successfully", "success")
    return redirect(url_for("tasks_bp.tasks_home"))


# Update task
@blueprint.route("/update/<int:task_id>", methods=["POST"])
@login_required
def update_task(task_id):
    name = request.form.get("name")
    if name:
        Task.update(task_id, name)
        flash("Task updated successfully", "success")
    return redirect(url_for("tasks_bp.tasks_home"))
