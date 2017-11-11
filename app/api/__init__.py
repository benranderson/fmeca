from flask import Blueprint

api = Blueprint('api', __name__)

from . import facilities, areas, components, subcomponents
