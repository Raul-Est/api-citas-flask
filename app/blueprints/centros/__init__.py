from flask import Blueprint

centros_bp = Blueprint("centros", __name__)

from . import routes  # noqa: E402, F401
