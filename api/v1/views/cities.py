#!/usr/bin/python3
"""New view for states object"""

from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State
from models.city import City


# states = storage.all(State).values()
# GET methods
@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    """Return all city objects"""
    all_cities = []
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    for city in state.cities:
        all_cities.append(city.to_dict())
    return jsonify(all_cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Get one city according to id"""
    city = storage.get(City, city_id)

    if not (city):
        abort(404)
    return jsonify(city.to_dict())


# DELETE method
@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Delete a city based on id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


# POST method
@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """Create a new city object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    imput = request.get_json()
    new_city = City(**imput)
    new_city.state_id = state.id
    new_city.save()
    return make_response(jsonify(new_city.to_dict()), 201)


# PUT method
@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Update a city using id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    imput = request.get_json()
    ig = ['id', 'created_at', 'updated_at']
    for k, v in imput.items():
        if k not in ig:
            setattr(city, k, v)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
