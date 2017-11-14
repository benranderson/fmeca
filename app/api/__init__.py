from flask import Blueprint

api = Blueprint('api', __name__)

from . import errors, index, facilities, areas, components, subcomponents, failure_modes
