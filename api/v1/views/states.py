#!/usr/bin/python3
""" view for states """


from api.v1.views import app_views
from flask import Flask, requests, jsonify, abort
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """retrieves all state objects """
    all_states = storage.all('State')
    return jsonify([obj.to_dict() for obj in all_states.values()])


@app_views.route(
        '/states/<state_id>', methods=['GET'],
        strict_slashes=False
        )
def get_state_id(state_id):
    """retrieves the state object of a specific id """
    get_state = storage.get('State', state_id)
    if not get_state:
        abort(404, 'Not found')
    return jsonify(get_state.to_dict())


@app_views.route(
        '/states/<state_id>', methods=['DELETE'],
        strict_slashes=False
        )
def delete_state(state_id):
    """ deletes a state object of a specific id """
    delete_state = storage.get('State', state_id)
    if not delete_state:
        abort(404, 'Not found')
    delete_state.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """ creates a new state"""
    create_state = request.get_json()
    if not create_state:
        abort(400, 'Not a JSON')
    if 'name' not in create_state:
        abort(400, 'Missing name')
    state = State(**create_state)
    storage.new(state)
    storage.save()
    return make_response(state.to_dict()), 201
