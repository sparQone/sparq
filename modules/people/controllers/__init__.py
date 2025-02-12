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
    "people_bp",
    __name__,
    template_folder="../views/templates",
    static_folder="../views/assets",
    static_url_path="/assets",
)

# Initialize filters with blueprint
init_filters(blueprint)

# Import routes after blueprint creation
from . import chat  # noqa: E402, F401
from . import docs  # noqa: E402, F401
from . import employee  # noqa: E402, F401
from . import forms  # noqa: E402, F401
from . import hiring  # noqa: E402, F401
from . import knowledge  # noqa: E402, F401
from . import onboarding  # noqa: E402, F401
from . import reimbursement  # noqa: E402, F401
from . import routes  # noqa: E402, F401
from . import scheduling  # noqa: E402, F401
from . import time_tracking  # noqa: E402, F401
