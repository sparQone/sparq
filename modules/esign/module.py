# -----------------------------------------------------------------------------
# sparQ
#
# Description:
#     E-Sign module class that implements e-signing and document management.
#     Handles route registration and blueprint registration.
#
# Copyright (c) 2025 remarQable LLC
#
# This software is released under an open-source license.
# See the LICENSE file for details.
# -----------------------------------------------------------------------------

class ESignModule:
    def register_blueprint(self, blueprint, url_prefix):
        self._blueprint = blueprint
        self._url_prefix = url_prefix
        
    def get_routes(self):
        return [(self._blueprint, self._url_prefix)] 