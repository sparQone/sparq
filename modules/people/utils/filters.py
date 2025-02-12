# -----------------------------------------------------------------------------
# sparQ
#
# Description:
#     People module filters for custom template filters.
#
# Copyright (c) 2025 remarQable LLC
#
# This software is released under an open-source license.
# See the LICENSE file for details.
# -----------------------------------------------------------------------------

from datetime import datetime
from flask import Blueprint
import humanize


def timeago_filter(value):
    """Convert datetime to '... time ago' text"""
    if not value:
        return ""

    now = datetime.utcnow()
    try:
        # Convert to datetime if string
        if isinstance(value, str):
            value = datetime.fromisoformat(value.replace("Z", "+00:00"))

        return humanize.naturaltime(now - value)
    except Exception as e:
        print(f"Error in timeago filter: {e}")  # Add logging
        return ""


def init_filters(app):
    """Initialize custom template filters"""
    # Register with both app and blueprint
    if isinstance(app, Blueprint):
        app.add_app_template_filter(timeago_filter, "timeago")
    else:
        app.jinja_env.filters["timeago"] = timeago_filter
        # Also register as a template filter
        app.template_filter("timeago")(timeago_filter)
