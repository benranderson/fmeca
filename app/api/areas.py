from flask import jsonify, request
from . import api
from .. import db
from ..models import Facility, Area
from ..decorators import json, paginate


@api.route('/areas/', methods=['GET'])
@json
@paginate('areas')
def get_areas():
    return Area.query


@api.route('/facilities/<int:id>/areas/', methods=['GET'])
@json
@paginate('areas')
def get_facility_areas(id):
    facility = Facility.query.get_or_404(id)
    return facility.areas


@api.route('/areas/<int:id>', methods=['GET'])
@json
def get_area(id):
    return Area.query.get_or_404(id)


@api.route('/facilities/<int:id>/areas/', methods=['POST'])
@json
def new_facility_area(id):
    facility = Facility.query.get_or_404(id)
    area = Area(facility=facility)
    area.import_data(request.json)
    db.session.add(area)
    db.session.commit()
    return {}, 201, {'Location': area.get_url()}


@api.route('/areas/<int:id>', methods=['PUT'])
@json
def edit_area(id):
    area = Area.query.get_or_404(id)
    area.import_data(request.json)
    db.session.add(area)
    db.session.commit()
    return {}


@api.route('/areas/<int:id>', methods=['DELETE'])
@json
def delete_area(id):
    area = Area.query.get_or_404(id)
    db.session.delete(area)
    db.session.commit()
    return {}
