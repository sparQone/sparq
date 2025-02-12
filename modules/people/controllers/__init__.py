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

# Import routes after blueprint creation to avoid circular imports
from . import chat  # noqa: F401, E402
from . import docs  # noqa: F401, E402
from . import employee  # noqa: F401, E402
from . import forms  # noqa: F401, E402
from . import hiring  # noqa: F401, E402
from . import knowledge  # noqa: F401, E402
from . import onboarding  # noqa: F401, E402
from . import reimbursement  # noqa: F401, E402
from . import routes  # noqa: F401, E402
from . import scheduling  # noqa: F401, E402
from . import time_tracking  # noqa: F401, E402
