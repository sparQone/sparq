# -----------------------------------------------------------------------------
# sparQ
#
# Description:
#     Clock module manifest defining module metadata, dependencies, and
#     configuration. Specifies clock functionality and time tracking.
#
# Copyright (c) 2025 RemarQable LLC
#
# This software is released under an open-source license.
# See the LICENSE file for details.
# -----------------------------------------------------------------------------

manifest = {
    'name': 'Clock',
    'version': '1.0',
    'main_route': '/clock',
    'icon_class': 'fa-regular fa-clock',
    'type': 'App',
    'color': '#6f42c1',  # Purple
    'depends': ['core'],
    'description': 'Digital clock demonstration app',
    'long_description': 'A simple digital clock application demonstrating real-time updates and basic module functionality. Includes time zone support and various display formats.'
}
