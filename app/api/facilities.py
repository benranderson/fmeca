from flask import jsonify, request
from . import api
from .. import db
from ..models import Facility
from ..decorators import json, paginate


@api.route("/facilities/", methods=['GET'])
@json
@paginate('facilities')
def get_facilities():
    return Facility.query


@api.route("/facilities/<int:id>", methods=['GET'])
@json
def get_facility(id):
    return Facility.query.get_or_404(id)


@api.route("/facilities/", methods=["POST"])
def new_facility():
    facility = Facility()
    facility.import_data(request.json)
    db.session.add(facility)
    db.session.commit()
    return jsonify({}), 201, {'Location': facility.get_url()}


@api.route("/facilities/<int:id>", methods=["PUT"])
def edit_facility(id):
    facility = Facility.query.get_or_404(id)
    facility.import_data(request.json)
    db.session.add(facility)
    db.session.commit()
    return jsonify({})


@api.route("/facilities/<int:id>", methods=["DELETE"])
def facility_delete(id):
    facility = Facility.query.get_or_404(id)
    db.session.delete(facility)
    db.session.commit()
    return jsonify({})
