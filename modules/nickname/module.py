from flask import Blueprint
from modules.module_manager import hookimpl
from .models import NicknameModel
from . import __manifest__

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
    def get_manifest(self):
        return __manifest__.manifest

    @hookimpl
    def modify_view(self):
        """Add nickname field to the core form"""
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