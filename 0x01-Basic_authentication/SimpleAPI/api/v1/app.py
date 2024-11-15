#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os
from api.v1.auth.auth import Auth


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None


auth_type = getenv('AUTH_TYPE', 'basic')
if auth_type == 'auth':
    auth = Auth()

if auth:
    from api.v1.auth.auth import Auth
    auth = Auth()

@app.before_request
def intercept_request():
    """
    checks every request for
    authentication and authorization
    before the request is handled
    """
    print('app.before_request method called')

    if auth is None:
        print('auth is None')
        return None

    auth_required = auth.require_auth(request.url, ['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/'])
    if auth_required:
        return

    # If auth is set, apply authentication checks
    if auth.authorization_header(request) is None:
        abort(401)  # Unauthorized if no authorization header

    if auth.current_user(request) is None:
        abort(403)  # Forbidden if current_user returns None (i.e., unauthorized user)


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(401)
def unauthorized(error) -> str:
    """
    unauthorized error handler
    """
    return jsonify({"error": "Unauthorized"}), 401

@app.errorhandler(403)
def access_forbidden(error) -> str:
    """
    access forbidden error handler
    """
    return jsonify({"error": "Forbidden"}), 403

if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
