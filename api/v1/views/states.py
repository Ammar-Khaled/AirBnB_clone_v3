#!/usr/bin/python3
"""
view for State objects
"""

from api.v1.views import app_views
from models.state import State
from models import storage
from flask import jsonify, abort, request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Return the list of all State objects."""
    all_states = []
    for state in storage.all(State).values():
        all_states.append(state.to_dict())
    return jsonify(all_states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Return the State object with state_id, or raise 404 error."""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Return the State object with state_id, or raise 404 error."""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({})


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """Create a State."""
    new_state = request.get_json()
    if not new_state:
        abort(400, 'Not a JSON')
    if 'name' not in new_state.keys():
        abort(400, 'Missing name')
    new_state_ins = State(**new_state)
    storage.new(new_state_ins)
    storage.save()
    return make_response(jsonify(new_state_ins.to_dict()), 201)
