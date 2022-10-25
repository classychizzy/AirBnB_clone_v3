#!/usr/bin/python3
"""New view for states object"""

from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.amenity import Amenity


# GET methods
@app_views.route('/amenities',
                 methods=['GET'], strict_slashes=False)
def get_amenities():
    """Return all amenity objects"""
    amenities = storage.all(Amenity).values()
    all_amenities = []
    for amenity in amenities:
        all_amenities.append(amenity.to_dict())
    return jsonify(all_amenities)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """Get one amenity according to id"""
    amenity = storage.get(Amenity, amenity_id)

    if not (amenity):
        abort(404)
    return jsonify(amenity.to_dict())


# DELETE method
@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """Delete an amenity based on id"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


# POST method
@app_views.route('/amenities',
                 methods=['POST'], strict_slashes=False)
def create_amenity():
    """Create a new amenity object"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    imput = request.get_json()
    new_amen = Amenity(**imput)
    new_amen.save()
    return make_response(jsonify(new_amen.to_dict()), 201)


# PUT method
@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """Update an amenity using id"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    imput = request.get_json()
    ig = ['id', 'created_at', 'updated_at']
    for k, v in imput.items():
        if k not in ig:
            setattr(amenity, k, v)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
