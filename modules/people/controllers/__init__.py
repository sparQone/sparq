# -----------------------------------------------------------------------------
# sparQ
#
# Description:
#     People module controllers.
#
# Copyright (c) 2025 remarQable LLC
#
# This software is released under an open-source license.
# See the LICENSE file for details.
# -----------------------------------------------------------------------------

from flask import Blueprint

from ..utils.filters import init_filters

# Create blueprint
blueprint = Blueprint(
    "people_bp", __name__, template_folder="../views/templates", static_folder="../views/assets"
)

# Register filters with the blueprint
init_filters(blueprint)

# Import routes after blueprint creation
from . import employee  # Changed from employee_routes to employee
from . import update
from . import hiring
from . import onboarding
from . import scheduling
from . import forms
from . import reimbursement
from . import docs
from . import knowledge
from . import time_tracking