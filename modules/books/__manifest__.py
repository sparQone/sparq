# -----------------------------------------------------------------------------
# sparQ
#
# Description:
#     Books module manifest defining module metadata, dependencies, and
#     configuration. Specifies bookkeeping and accounting features for
#     small business management.
#
# Copyright (c) 2025 remarQable LLC
#
# This software is released under an open-source license.
# See the LICENSE file for details.
# -----------------------------------------------------------------------------

manifest = {
    'name': 'Books',
    'version': '1.0',
    'main_route': '/books',
    'icon_class': 'fa-solid fa-book',
    'type': 'App',
    'color': '#20c997',  # Teal
    'depends': ['core'],
    'description': 'Simple bookkeeping for small businesses',
    'long_description': 'Easy-to-use accounting system designed for small businesses. Track income, expenses, invoices, and generate basic financial reports. Perfect for entrepreneurs and small business owners.'
} 