#!/usr/bin/env python3
"""App module
"""
from flask import (
    Flask, jsonify, request, abort, make_response, redirect, url_for
    )
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def welcome() -> str:
    """GET /
    Return:
      - welcome message : {"message": "Bienvenue"}
    """
    return jsonify({"message": "Bienvenue"})


# sign up
@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """POST /users
    JSON body:
        - email
        - password
    Return:
        - {"email": "<registered email>", "message": "user created"} if success
        - {"message": "email already registered"} if error
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


# sign in / log in
@app.route('/sessions', methods=['POST'], strict_slashes=False)
def sessions() -> str:
    """POST /sessions
    JSON body:
        - email
        - password
    Set-Cookie:
        - session_id = <session_id>
    Return:
        - {"email": "<user email>", "message": "logged in"} if success
        - abort with a 401 if error
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response = make_response(
            jsonify({"email": email, "message": "logged in"})
            )
        response.set_cookie('session_id', session_id)
        return response
    abort(401)


# sign out / log out
@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def delete_session() -> str:
    """DELETE /sessions
    JSON body:
        - session_id
    Return:
        - redirect to 'welcome' endpoint if success
        - abort with a 403 if error
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect(url_for('welcome'))
    abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """GET /profile
    JSON body:
        - session_id
    Return:
        - {"email": "<user email>"} if success
        - abort with a 403 if error
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email})
    abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> str:
    """POST /reset_password
    JSON body:
        - email
    Return:
        - {"email": "<user email>", "reset_token": "<reset_token>"} if success
        - abort with a 403 if error
    """
    email = request.form.get('email')
    try:
        reset_token = AUTH.get_reset_password_token(email)
        if reset_token:
            return jsonify({"email": email, "reset_token": reset_token})
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    """PUT /reset_password
    JSON body:
        - email
        - reset_token
        - new_password
    Return:
        - {"email": "<user email>", "message": "Password updated"} if success
        - abort with a 403 if error
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"})
    except ValueError:
        abort(403)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
