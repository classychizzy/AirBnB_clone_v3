#!/usr/bin/python3
"""New view for places object"""

from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.user import User


# states = storage.all(State).values()
# GET methods
@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """Return all place objects"""
    all_places = []
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    for place in city.places:
        all_places.append(place.to_dict())
    return jsonify(all_places)


@app_views.route('/places/<place_id>',
                 methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Get one place according to id"""
    place = storage.get(Place, place_id)

    if not (place):
        abort(404)
    return jsonify(place.to_dict())


# DELETE method
@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Delete a place based on id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


# POST method
@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Create a new Place object"""
    city = storage.get(City, city_id)
    imput = request.get_json()
    user = storage.get(User, imput['user_id'])
    if not city or not user:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")
    # imput = request.get_json()
    # user = storage.get(User, imput['user_id'])
    new_place = Place(**imput)
    new_place.save()
    return make_response(jsonify(new_place.to_dict()), 201)


# PUT method
@app_views.route('/places/<place_id>',
                 methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Update a place using id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    imput = request.get_json()
    ig = ['id', 'user_id', 'city_id',
          'created_at', 'updated_at']
    for k, v in imput.items():
        if k not in ig:
            setattr(place, k, v)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
