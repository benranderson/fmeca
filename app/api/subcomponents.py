
from flask import jsonify, request
from . import api
from .. import db
from ..models import Component, SubComponent


@api.route('/subcomponents/', methods=['GET'])
def get_subcomponents():
    return jsonify({
        'subcomponents': [subcomponent.get_url() for subcomponent in SubComponent.query.all()]
    })


@api.route('/components/<int:id>/subcomponents/', methods=['GET'])
def get_component_subcomponents(id):
    component = Component.query.get_or_404(id)
    return jsonify({
        'subcomponents': [subcomponent.get_url() for subcomponent in component.subcomponents.all()]
    })


@api.route('/subcomponents/<int:id>', methods=['GET'])
def get_subcomponent(id):
    return jsonify(SubComponent.query.get_or_404(id).export_data())


@api.route('/components/<int:id>/subcomponents/', methods=['POST'])
def new_component_subcomponent(id):
    component = Component.query.get_or_404(id)
    subcomponent = SubComponent(component=component)
    subcomponent.import_data(request.json)
    db.session.add(subcomponent)
    db.session.commit()
    return jsonify({}), 201, {'Location': subcomponent.get_url()}


@api.route('/subcomponents/<int:id>', methods=['PUT'])
def edit_subcomponent(id):
    subcomponent = SubComponent.query.get_or_404(id)
    subcomponent.import_data(request.json)
    db.session.add(subcomponent)
    db.session.commit()
    return jsonify({})


@api.route('/subcomponents/<int:id>', methods=['DELETE'])
def delete_subcomponent(id):
    subcomponent = SubComponent.query.get_or_404(id)
    db.session.delete(subcomponent)
    db.session.commit()
    return jsonify({})
