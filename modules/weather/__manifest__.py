# -----------------------------------------------------------------------------
# sparQ
#
# Description:
#     Weather module manifest defining module metadata, dependencies, and
#     configuration. Specifies integration with core module and weather
#     service requirements.
#
# Copyright (c) 2025 RemarQable LLC
#
# This software is released under an open-source license.
# See the LICENSE file for details.
# -----------------------------------------------------------------------------

manifest = {
    'name': 'Weather',
    'version': '1.0',
    'main_route': '/weather',
    'icon_class': 'fa-solid fa-cloud-sun',
    'type': 'App',
    'color': '#0dcaf0',  # Cyan
    'depends': ['core'],
    'description': 'Local weather information',
    'long_description': 'Real-time weather updates and forecasts for your location. Features current conditions, hourly forecasts, and severe weather alerts. Customizable for multiple locations.'
}