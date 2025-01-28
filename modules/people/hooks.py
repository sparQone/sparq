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
    def process_new_employee(self, form_data):
        """Process additional employee data from form submission.
        Args:
            form_data: The submitted form data
        """
        pass 