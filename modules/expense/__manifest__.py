# -----------------------------------------------------------------------------
# sparQ
#
# Description:
#     Expense module manifest defining module metadata, dependencies, and
#     configuration. Specifies expense tracking features and integration
#     with accounting system.
#
# Copyright (c) 2025 RemarQable LLC
#
# This software is released under an open-source license.
# See the LICENSE file for details.
# -----------------------------------------------------------------------------

manifest = {
    'name': 'Expense',
    'version': '1.0',
    'main_route': '/expense',
    'icon_class': 'fa-solid fa-receipt',
    'type': 'App',
    'color': '#198754',  # Green
    'depends': ['core', 'people'],
    'description': 'Expense tracking and reimbursement',
    'long_description': 'Complete expense management solution for tracking business expenses and processing employee reimbursements. Features receipt scanning, approval workflows, and expense report generation.'
} 