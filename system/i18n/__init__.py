# -----------------------------------------------------------------------------
# sparQ
#
# Description:
#     Translation module that provides core translation functionality including
#     preloading translations, custom translation function, and formatting functions.
#
# Copyright (c) 2025 remarQable LLC
#
# This software is released under an open-source license.
# See the LICENSE file for details.
# -----------------------------------------------------------------------------

from .translation import preload_translations
from .translation import translate

__all__ = ["translate", "preload_translations"]
