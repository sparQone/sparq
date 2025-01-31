# -----------------------------------------------------------------------------
# sparQ
#
# Description:
#     Database configuration and base model setup for SQLAlchemy integration.
#     Provides the central database instance used throughout the application.
#
# Copyright (c) 2025 RemarQable LLC
#
# This software is released under an open-source license.
# See the LICENSE file for details.
# -----------------------------------------------------------------------------

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base) 