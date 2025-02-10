# -----------------------------------------------------------------------------
# sparQ
#
# Description:
#     People module decorators.
#
# Copyright (c) 2025 remarQable LLC
#
# This software is released under an open-source license.
# See the LICENSE file for details.
# -----------------------------------------------------------------------------

from functools import wraps
from flask import abort
from flask_login import current_user

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function 