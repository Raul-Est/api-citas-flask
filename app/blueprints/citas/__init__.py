from flask import Blueprint

citas_bp = Blueprint("citas", __name__)

from . import routes  # noqa: E402, F401
