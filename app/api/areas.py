from flask import jsonify, request
from . import api
from .. import db
from ..models import Facility, Area


@api.route('/areas/', methods=['GET'])
def get_areas():
    return jsonify({'areas': [area.get_url() for area in Area.query.all()]})


@api.route('/facilities/<int:id>/areas/', methods=['GET'])
def get_facility_areas(id):
    facility = Facility.query.get_or_404(id)
    return jsonify({'areas': [area.get_url() for area in
                              facility.areas.all()]})


@api.route('/areas/<int:id>', methods=['GET'])
def get_area(id):
    return jsonify(Area.query.get_or_404(id).export_data())


@api.route('/facilities/<int:id>/areas/', methods=['POST'])
def new_facility_area(id):
    facility = Facility.query.get_or_404(id)
    area = Area(facility=facility)
    area.import_data(request.json)
    db.session.add(area)
    db.session.commit()
    return jsonify({}), 201, {'Location': area.get_url()}


@api.route('/areas/<int:id>', methods=['PUT'])
def edit_area(id):
    area = Area.query.get_or_404(id)
    area.import_data(request.json)
    db.session.add(area)
    db.session.commit()
    return jsonify({})


@api.route('/areas/<int:id>', methods=['DELETE'])
def delete_area(id):
    area = Area.query.get_or_404(id)
    db.session.delete(area)
    db.session.commit()
    return jsonify({})
