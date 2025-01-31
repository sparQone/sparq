# -----------------------------------------------------------------------------
# sparQ
#
# Description:
#     People module manifest defining module metadata, dependencies, and
#     configuration. Specifies HR and employee management features and
#     integration requirements.
#
# Copyright (c) 2025 RemarQable LLC
#
# This software is released under an open-source license.
# See the LICENSE file for details.
# -----------------------------------------------------------------------------

manifest = {
    'name': 'People',
    'version': '1.0',
    'main_route': '/people',
    'icon_class': 'fa-solid fa-users',
    'type': 'App',
    'color': '#0d6efd',  # Module's color
    'depends': ["core"],
    'description': 'Employee management and HR tools',
    'long_description': 'Comprehensive HR management system including employee profiles, onboarding, time tracking, scheduling, and document management. Streamline your HR operations and employee management workflows.'
} 