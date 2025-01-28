from flask import Blueprint
from system.module.module_manager import hookimpl
from .models import NicknameModel

class NicknameModule:
    def __init__(self):
        self.blueprint = Blueprint('nickname_bp', __name__)
        self.setup_routes()

    def setup_routes(self):
        @self.blueprint.route("/")
        def nickname_home():
            return {"message": "Nickname Module Home"}

    @hookimpl
    def get_routes(self):
        return [(self.blueprint, "/nickname")]

    @hookimpl
    def modify_new_employee_form(self):
        """Add nickname field to new employee form"""
        js = """
        <script>
            function addField(fieldHtml) {
                // Find the last name field's parent div
                const lastNameField = document.querySelector('#last_name').closest('.mb-3');
                // Create new div for nickname field
                const div = document.createElement('div');
                div.className = 'mb-3';
                div.innerHTML = fieldHtml.trim();
                // Insert after the last name field
                lastNameField.insertAdjacentElement('afterend', div);
            }

            document.addEventListener('DOMContentLoaded', function() {
                addField(`
                    <label for="nickname" class="form-label">Nickname</label>
                    <input type="text" 
                           class="form-control" 
                           id="nickname" 
                           name="nickname" 
                           placeholder="Enter nickname">
                `);
            });
        </script>
        """
        return [js]

    @hookimpl
    def process_new_employee(self, form_data):
        """Process nickname when new employee is created"""
        if 'nickname' in form_data:
            print(f"Nickname plugin: Processing nickname '{form_data['nickname']}'")

    @hookimpl
    def modify_core_form(self):
        """Add nickname field specifically to the core form"""
        js = """
        <script>
            function addField(fieldHtml) {
                const additionalFields = document.getElementById('form-actions');
                const div = document.createElement('div');
                div.className = 'mb-3';
                div.innerHTML = fieldHtml.trim();
                additionalFields.parentNode.insertBefore(div, additionalFields);
            }

            // Add nickname field when page loads
            document.addEventListener('DOMContentLoaded', function() {
                addField(`
                    <label for="nickname" class="form-label">Nickname</label>
                    <input type="text" 
                           class="form-control" 
                           id="nickname" 
                           name="nickname" 
                           placeholder="Johnny"
                           value="Johnny">
                `);
            });
        </script>
        """
        return [js]

    @hookimpl
    def get_model(self, base_model):
        """Return nickname model that extends base model"""
        return [NicknameModel()] 