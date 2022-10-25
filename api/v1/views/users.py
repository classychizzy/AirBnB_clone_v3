#!/usr/bin/python3
"""New view for users object"""

from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.user import User


# GET methods
@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Return all user objects"""
    users = storage.all(User).values()
    all_users = []
    for user in users:
        all_users.append(user.to_dict())
    return jsonify(all_users)


@app_views.route('/users/<user_id>',
                 methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Get one user according to id"""
    user = storage.get(User, user_id)

    if not (user):
        abort(404)
    return jsonify(user.to_dict())


# DELETE method
@app_views.route('/users/<user_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Delete a user based on id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


# POST method
@app_views.route('/users',
                 methods=['POST'], strict_slashes=False)
def create_user():
    """Create a new user object"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'email' not in request.get_json():
        abort(400, description="Missing email")
    if 'password' not in request.get_json():
        abort(400, description="Missing password")
    imput = request.get_json()
    new_user = User(**imput)
    new_user.save()
    return make_response(jsonify(new_user.to_dict()), 201)


# PUT method
@app_views.route('/users/<user_id>',
                 methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Update a user using id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    imput = request.get_json()
    ig = ['id', 'email', 'created_at', 'updated_at']
    for k, v in imput.items():
        if k not in ig:
            setattr(user, k, v)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
