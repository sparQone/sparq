from flask import Blueprint

from ..utils.filters import init_filters

# Create blueprint
blueprint = Blueprint(
    "people_bp", __name__, template_folder="../views/templates", static_folder="../views/assets"
)

# Register filters with the blueprint
init_filters(blueprint)

# Import routes to register them with blueprint
from . import employee
from . import update
from . import docs
from . import forms
from . import hiring
from . import onboarding
from . import scheduling
from . import reimbursement
from . import knowledge
from . import time_tracking
from . import dashboard