# -----------------------------------------------------------------------------
# sparQ
#
# Description:
#     Books module class that implements accounting and bookkeeping
#     functionality. Handles route registration and database initialization
#     for the books management system.
#
# Copyright (c) 2025 remarQable LLC
#
# This software is released under an open-source license.
# See the LICENSE file for details.
# -----------------------------------------------------------------------------


class BooksModule:
    def register_blueprint(self, blueprint, url_prefix):
        self._blueprint = blueprint
        self._url_prefix = url_prefix

    def get_routes(self):
        return [(self._blueprint, self._url_prefix)]
