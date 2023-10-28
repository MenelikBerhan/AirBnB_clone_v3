#!/usr/bin/python3
"""Module containing a Flask Blueprint routes that handles
all default RESTFul API actions for Amenity resource"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from markupsafe import escape
from models import storage
from models.amenity import Amenity


def retrive_object(cls, id):
    """Retrives a resource based on given class and id."""
    obj = storage.get(cls, escape(id))
    if obj is None:
        abort(404)
    return (obj)


def validate_request_json(request):
    """Checks validity of request's json content"""
    req_json = request.get_json(silent=True)
    if req_json is None:
        abort(jsonify({"error": "Not a JSON"}), 400)
    if request.method == 'POST' and 'name' not in req_json:
        abort(jsonify({"error": "Missing name"}), 400)
    return (req_json)


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def amenities_get(amenity_id=None):
    """Returns an Amenity with given id, or all amenities if no id is given"""
    if amenity_id is None:
        amenities = storage.all(Amenity).values()
        return (jsonify([amenity.to_dict() for amenity in amenities]))
    obj = retrive_object(Amenity, escape(amenity_id))
    return (jsonify(obj.to_dict()))


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def amenities_delete(amenity_id):
    """Deletes an Amenity resource based on given id"""
    obj = retrive_object(Amenity, escape(amenity_id))
    storage.delete(obj)
    storage.save()
    return (jsonify({}))


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def amenities_post():
    """Creates an Amenity resource if request content is valid."""
    req_json = validate_request_json(request)
    new_amenity = Amenity(**req_json)
    new_amenity.save()
    return (jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def amenities_put(amenity_id):
    """Updates an Amenity resource of given id if request content is valid."""
    obj = retrive_object(Amenity, escape(amenity_id))
    req_json = validate_request_json(request)
    ignore = ['id', 'created_at', 'updated_at']
    for key, value in req_json.items():
        if key not in ignore:
            setattr(obj, key, value)
    obj.save()
    return (jsonify(obj.to_dict()))
