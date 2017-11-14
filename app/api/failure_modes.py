from flask import jsonify, request
from . import api
from .. import db
from ..models import SubComponent, Consequence, FailureMode
from ..decorators import json, paginate


@api.route('/subcomponents/<int:id>/failure_modes/', methods=['GET'])
@json
@paginate('failure_modes')
def get_subcomponent_failure_modes(id):
    subcomponent = SubComponent.query.get_or_404(id)
    return subcomponent.failure_modes


@api.route('/failure_modes/<int:id>', methods=['GET'])
@json
def get_failure_mode(id):
    return FailureMode.query.get_or_404(id)


@api.route('/components/<int:id>/subcomponents/', methods=['POST'])
@json
def new_subcomponent_failure_mode(id):
    subcomponent = SubComponent.query.get_or_404(id)
    failure_mode = FailureMode(subcomponent=subcomponent)
    failure_mode.import_data(request.json)
    db.session.add(failure_mode)
    db.session.commit()
    return {}, 201, {'Location': failure_mode.get_url()}


@api.route('/failure_modes/<int:id>', methods=['PUT'])
@json
def edit_failure_mode(id):
    failure_mode = FailureMode.query.get_or_404(id)
    failure_mode.import_data(request.json)
    db.session.add(failure_mode)
    db.session.commit()
    return {}


@api.route('/failure_modes/<int:id>', methods=['DELETE'])
@json
def delete_failure_mode(id):
    failure_mode = FailureMode.query.get_or_404(id)
    db.session.delete(failure_mode)
    db.session.commit()
    return {}
