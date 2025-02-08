# -----------------------------------------------------------------------------
# sparQ
#
# Description:
#     Appointments module manifest defining module metadata, dependencies,
#     and configuration. Specifies scheduling features and calendar
#     integration requirements.
#
# Copyright (c) 2025 remarQable LLC
#
# This software is released under an open-source license.
# See the LICENSE file for details.
# -----------------------------------------------------------------------------

manifest = {
    "name": "Appointments",
    "version": "1.0",
    "main_route": "/appointments",
    "icon_class": "fa-solid fa-calendar-check",
    "type": "App",
    "color": "#6f42c1",  # Purple
    "depends": ["core"],
    "description": "Appointment scheduling and calendar management",
    "long_description": "Complete appointment booking system with calendar integration, availability management, and automated reminders. Perfect for service-based businesses and professional scheduling.",
}
