# -----------------------------------------------------------------------------
# sparQ
#
# Description:
#     E-Sign module manifest defining module metadata, dependencies, and
#     configuration. Specifies e-signing and document management features.
#
# Copyright (c) 2025 remarQable LLC
#
# This software is released under an open-source license.
# See the LICENSE file for details.
# -----------------------------------------------------------------------------
manifest = {
    'name': 'E-Sign',
    'version': '1.0',
    'depends': ['core'],
    'main_route': '/esign',
    'icon_class': 'fa-regular fa-file-signature',
    'type': 'App',
    'color': '#007bff',  # Blue color
    'description': 'Electronic document signing',
    'long_description': 'Secure electronic signature solution for your documents. Create, send, and track digital signatures for contracts, agreements, and other important documents.'
} 

