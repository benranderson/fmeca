from flask import jsonify, request
from . import api
from .. import db
from ..models import Component, SubComponent
from ..decorators import json, paginate


@api.route('/components/<int:id>/subcomponents/', methods=['GET'])
@json
@paginate('subcomponents')
def get_component_subcomponents(id):
    component = Component.query.get_or_404(id)
    return component.subcomponents


@api.route('/subcomponents/<int:id>', methods=['GET'])
@json
def get_subcomponent(id):
    return SubComponent.query.get_or_404(id)


@api.route('/components/<int:id>/subcomponents/', methods=['POST'])
@json
def new_component_subcomponent(id):
    component = Component.query.get_or_404(id)
    subcomponent = SubComponent(component=component)
    subcomponent.import_data(request.json)
    db.session.add(subcomponent)
    db.session.commit()
    return {}, 201, {'Location': subcomponent.get_url()}


@api.route('/subcomponents/<int:id>', methods=['PUT'])
@json
def edit_subcomponent(id):
    subcomponent = SubComponent.query.get_or_404(id)
    subcomponent.import_data(request.json)
    db.session.add(subcomponent)
    db.session.commit()
    return {}


@api.route('/subcomponents/<int:id>', methods=['DELETE'])
@json
def delete_subcomponent(id):
    subcomponent = SubComponent.query.get_or_404(id)
    db.session.delete(subcomponent)
    db.session.commit()
    return {}
