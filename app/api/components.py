from flask import jsonify, request
from . import api
from .. import db
from ..models import Area, Component
from ..decorators import json, paginate


@api.route("/areas/<int:id>/components/", methods=['GET'])
@json
@paginate('components')
def get_area_components(id):
    area = Area.query.get_or_404(id)
    return area.components


@api.route("/components/<int:id>", methods=['GET'])
@json
def get_component(id):
    return Component.query.get_or_404(id)


@api.route("/areas/<int:id>/components/", methods=["POST"])
@json
def new_area_component(id):
    area = Area.query.get_or_404(id)
    component = Component(area=area)
    component.import_data(request.json)
    db.session.add(component)
    db.session.commit()
    return {}, 201, {'Location': component.get_url()}


@api.route("/components/<int:id>", methods=["PUT"])
@json
def edit_component(id):
    component = Component.query.get_or_404(id)
    component.import_data(request.json)
    db.session.add(component)
    db.session.commit()
    return {}


@api.route("/components/<int:id>", methods=["DELETE"])
@json
def component_delete(id):
    component = Component.query.get_or_404(id)
    db.session.delete(component)
    db.session.commit()
    return {}
