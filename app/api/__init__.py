from flask import Blueprint

api = Blueprint('api', __name__)

from . import index, facilities, areas, components, subcomponents, failure_modes
