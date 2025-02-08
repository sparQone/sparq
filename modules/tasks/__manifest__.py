# -----------------------------------------------------------------------------
# sparQ
#
# Description:
#     Tasks module manifest defining module metadata, dependencies, and
#     configuration. Specifies task and to-do management features.
#
# Copyright (c) 2025 remarQable LLC
#
# This software is released under an open-source license.
# See the LICENSE file for details.
# -----------------------------------------------------------------------------

manifest = {
    "name": "Tasks",
    "version": "1.0",
    "main_route": "/tasks",
    "icon_class": "fa-regular fa-check-square",
    "type": "App",
    "color": "#007bff",  # Blue color
    "depends": ["core"],
    "description": "Task and to-do management",
    "long_description": "Simple yet powerful task management system. Create, organize, and track tasks with ease. Perfect for personal to-dos or team task management.",
}
