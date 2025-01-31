# -----------------------------------------------------------------------------
# sparQ
#
# Description:
#     People module hook specifications for plugin system integration.
#     Defines hooks for employee lifecycle events and data management.
#
# Copyright (c) 2025 RemarQable LLC
#
# This software is released under an open-source license.
# See the LICENSE file for details.
# -----------------------------------------------------------------------------

from system.module.module_manager import hookspec

class PeopleHookSpecs:
    @hookspec
    def modify_new_employee_form(self):
        """Add custom elements to the new employee form.
        Returns:
            list: List of HTML strings to be inserted into the new employee form
        """
        pass

    @hookspec
    def process_new_employee(self, form_data, employee):
        """Process additional employee data from form submission.
        Args:
            form_data: The submitted form data
            employee: The newly created employee instance
        """
        pass

    @hookspec
    def modify_edit_employee_form(self, employee):
        """Add additional fields to employee edit form.
        Args:
            employee: The employee being edited
        Returns:
            list: List of HTML strings to be inserted into the edit form
        """
        pass

    @hookspec
    def process_employee_update(self, form_data, employee):
        """Process additional form data when employee is updated.
        Args:
            form_data: The submitted form data
            employee: The employee being updated
        """
        pass

    @hookspec
    def employee_created(self, employee):
        """Called after a new employee is created"""
        pass

    @hookspec
    def employee_updated(self, employee, changes):
        """Called after an employee is updated"""
        pass 