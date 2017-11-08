from flask import jsonify, request
from . import api
from ..models import Component
from .. import db


@api.route("/components/", methods=['GET'])
def get_components():
    return jsonify({
        'components': [component.get_url() for component in Component.query.all()]
    })


@api.route("/components/<int:id>", methods=['GET'])
def get_component(id):
    return jsonify(Component.query.get_or_404(id).export_data())


@api.route("/components/", methods=["POST"])
def new_component():
    component = Component()
    component.import_data(request.json)
    db.session.add(component)
    db.session.commit()
    return jsonify({}), 201, {'Location': component.get_url()}


@api.route("/components/<int:id>", methods=["PUT"])
def edit_component(id):
    component = Component.query.get_or_404(id)
    component.import_data(request.json)
    db.session.add(component)
    db.session.commit()
    return jsonify({})


@api.route("/components/<int:id>", methods=["DELETE"])
def component_delete(id):
    component = Component.query.get_or_404(id)
    db.session.delete(component)
    db.session.commit()
    return jsonify({})
