#!/usr/bin/python3
"""New view for states object"""

from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State


states = storage.all(State).values()


# GET methods
@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Return all state objects"""
    all_states = []
    for state in states:
        all_states.append(state.to_dict())
    return jsonify(all_states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Get one state according to id"""
    state = storage.get(State, state_id)

    if not (state):
        abort(404)
    return jsonify(state.to_dict())


# DELETE method
@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Delete a state based on id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


# POST method
@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Create a new state object"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    imput = request.get_json()
    new_state = State(**imput)
    new_state.save()
    return make_response(jsonify(new_state.to_dict()), 201)


# PUT method
@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Update a state using id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    imput = request.get_json()
    ig = ['id', 'created_at', 'updated_at']
    for k, v in imput.items():
        if k not in ig:
            setattr(state, k, v)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
