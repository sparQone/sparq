# -----------------------------------------------------------------------------
# sparQ
#
# Description:
#     Nickname module manifest defining module metadata, dependencies, and
#     configuration. Specifies nickname functionality and integration with
#     employee profiles.
#
# Copyright (c) 2025 remarQable LLC
#
# This software is released under an open-source license.
# See the LICENSE file for details.
# -----------------------------------------------------------------------------
manifest = {
    "name": "Nickname",
    "version": "1.0",
    "main_route": "/nickname",
    "icon_class": "fa-solid fa-tag",
    "type": "Extension",
    "color": "#dc3545",  # Red
    "depends": ["core", "people"],
    "description": "Add nicknames to employee profiles",
    "long_description": "Example extension module that demonstrates module modification capabilities. Adds nickname fields to employee profiles and showcases the plugin system for extending existing functionality.",
    "meta_tags": {"viewport": "width=device-width, initial-scale=1.0"},
}
