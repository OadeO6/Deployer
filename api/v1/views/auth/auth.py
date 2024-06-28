"""
login and logout views
"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request

@app_views.route('/tokken', method=['GET'], strict_slashes=False)
def get_tokken():
    res = make_response(jsonify({}), 200)
    return res
