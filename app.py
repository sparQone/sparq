import warnings
warnings.filterwarnings('ignore', message='urllib3 v2 only supports OpenSSL 1.1.1+')


from flask import Flask, request, jsonify, redirect, url_for
from system.module.module_loader import ModuleLoader

def create_app():
    app = Flask(__name__)
    
    # Initialize module loader
    module_loader = ModuleLoader()
    
    # Make module_loader available to the app
    app.module_loader = module_loader
    
    # Load all modules
    module_loader.load_modules()
    
    # Get all module manifests
    manifests = []
    for result in module_loader.pm.hook.get_manifest():
        if result:
            manifests.extend(result if isinstance(result, list) else [result])
    
    # Store manifests in app config
    app.config['INSTALLED_MODULES'] = manifests
    
    # Register all module routes
    for results in module_loader.pm.hook.get_routes():
        if results:
            for blueprint, url_prefix in results:
                app.register_blueprint(blueprint, url_prefix=url_prefix)
    
    # Register Jinja filters from core module
    core_module = next(
        (m for m in module_loader.pm.get_plugins() 
         if m.__class__.__name__ == 'CoreModule'), 
        None
    )
    if core_module:
        app.jinja_env.filters['icon_class'] = core_module.icon_class_filter

    
    
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
