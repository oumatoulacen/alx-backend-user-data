#!/usr/bin/env python3
""" DocDocDocDocDocDoc
"""
from os import getenv
from flask import abort, jsonify, request
from models.user import User
from api.v1.views import app_views


@app_views.route('auth_session/login', methods=['POST'], strict_slashes=False)
def login_session():
    """ POST /api/v1/auth_session/login
    Return:
      - User object JSON represented
      - 400 if email is missing
      - 400 if email is not a string
      - 400 if password is missing
      - 400 if password is not a string
      - 401 if email doesn't match any User
      - 401 if password is invalid
    """
    email = request.form.get('email')
    if email is None or type(email) is not str or email == "":
        return jsonify({"error": "email missing"}), 400
    password = request.form.get('password')
    if password is None or type(password) is not str:
        return jsonify({"error": "password missing"}), 400
    user = User.search({'email': email})
    if user is None or not user:
        return jsonify({"error": "no user found for this email"}), 404
    if not user[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.auth.session_auth import SessionAuth
    from api.v1.auth.session_exp_auth import SessionExpAuth
    if getenv('AUTH_TYPE') == 'session_exp_auth':
        session_id = SessionExpAuth().create_session(user[0].id)
    else:
        session_id = SessionAuth().create_session(user[0].id)
    response = jsonify(user[0].to_json())
    response.set_cookie(getenv('SESSION_NAME'), session_id)
    return response


@app_views.route('auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout():
    """ DELETE /api/v1/auth_session/logout
    Return:
      - 200 on success
    """
    from api.v1.auth.session_auth import SessionAuth
    if SessionAuth().destroy_session(request):
        return jsonify({}), 200
    abort(404)
