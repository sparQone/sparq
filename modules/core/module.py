from flask import Blueprint, jsonify, current_app, render_template, request, redirect, url_for
from system.module.module_manager import hookimpl
from .models import Model
from . import __manifest__

class CoreModule:
    def __init__(self):
        self.blueprint = Blueprint(
            'core_bp', __name__,
            template_folder='templates'
        )
        self.setup_routes()

    def setup_routes(self):
        @self.blueprint.route("/")
        def home():
            """Render the apps dashboard as the home page"""
            installed = current_app.config.get('INSTALLED_MODULES', [])
            return render_template("apps.html", installed_modules=installed)

        @self.blueprint.route("/core")
        def core_home():
            """Core module home page with form"""
            # Get plugin HTML and ensure it's a list of strings
            plugin_html = current_app.module_loader.pm.hook.modify_view()
            if not plugin_html:
                plugin_html = []
            
            # Flatten the list of lists into a single list of strings
            flattened_html = [item for sublist in plugin_html for item in (sublist if isinstance(sublist, list) else [sublist])]
            
            # Join all plugin HTML fragments with newlines for better formatting
            combined_plugin_html = "\n".join(filter(None, flattened_html))
            
            return render_template("form.html", plugin_html=combined_plugin_html)

        @self.blueprint.route("/save", methods=['POST'])
        def save():
            """Handle form submission"""
            form_data = {
                'firstname': request.form.get('firstname', ''),
                'lastname': request.form.get('lastname', ''),
                'email': request.form.get('email', '')
            }
            
            # Get base model
            base_model = Model()
            
            # Get plugin models
            plugin_models = current_app.module_loader.pm.hook.get_model(base_model=base_model)
            print("Plugin models:", plugin_models)  # Debug print
            
            # Use the last plugin model if available, otherwise use base model
            model = plugin_models[-1][0] if plugin_models else base_model
            print("Using model:", model.__class__.__name__)  # Debug print
            
            # Save the data
            model.save(request.form)  # Pass the entire form data to let plugins handle their fields
            return redirect(url_for('core_bp.core_home'))

    def icon_class_filter(self, mod):
        """Returns a Font Awesome class string based on module name"""
        name = mod.get("name", "").lower()
        if "core" in name:
            return "fa-solid fa-home"
        elif "clock" in name:
            return "fa-regular fa-clock"
        elif "weather" in name:
            return "fa-solid fa-cloud-sun-rain"
        elif "nickname" in name:
            return "fa-solid fa-user-tag"
        return "fa-solid fa-puzzle-piece"

    @hookimpl
    def get_routes(self):
        return [(self.blueprint, "/")]

    @hookimpl
    def modify_view(self):
        """Allow other modules to inject fields"""
        return []

