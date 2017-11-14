from flask import jsonify
from . import api


@api.route('/', methods=['GET'])
def index():
    return jsonify("Welcome to the fmeca API. Check out '/api/facilities/'.")
