from flask import jsonify, request
from . import api
from .. import db
from ..models import Component, Consequence
from ..decorators import json, paginate


@api.route('/components/<int:id>/consequences/', methods=['GET'])
@json
@paginate('consequences')
def get_component_consequences(id):
    component = Component.query.get_or_404(id)
    return component.consequences


@api.route('/consequences/<int:id>', methods=['GET'])
@json
def get_consequence(id):
    return Consequence.query.get_or_404(id)


@api.route('/components/<int:id>/consequences/', methods=['POST'])
@json
def new_component_consequence(id):
    component = Component.query.get_or_404(id)
    consequence = Consequence(component=component)
    consequence.import_data(request.json)
    db.session.add(consequence)
    db.session.commit()
    return {}, 201, {'Location': consequence.get_url()}


@api.route('/consequences/<int:id>', methods=['PUT'])
@json
def edit_consequence(id):
    consequence = Consequence.query.get_or_404(id)
    consequence.import_data(request.json)
    db.session.add(consequence)
    db.session.commit()
    return {}


@api.route('/consequences/<int:id>', methods=['DELETE'])
@json
def delete_consequence(id):
    consequence = Consequence.query.get_or_404(id)
    db.session.delete(consequence)
    db.session.commit()
    return {}
