#!/usr/bin/env python3
'''End-to-end integration test module'''
from auth import Auth
from user import User
import bcrypt
import requests

# This is temporary to avoid the user already exist error:
import os
# os.remove('a.db')


AUTH = Auth()


def register_user(EMAIL, PASSWD):
    '''Test registration'''
    r = requests.post(
        'http://localhost:5000/users',
        data={'email': EMAIL, 'password': PASSWD}
        )
    assert r.status_code == 200
    r = requests.post(
        'http://localhost:5000/users',
        data={'email': EMAIL, 'password': PASSWD}
        )
    assert r.status_code == 400
    # user = AUTH.register_user(EMAIL, PASSWD)
    # assert user.email == EMAIL
    # assert user._User__password != PASSWD
    # assert AUTH._Auth__db.find_user_by(email=EMAIL) == user


def log_in_wrong_password(EMAIL, NEW_PASSWD):
    '''Test login with wrong password'''
    r = requests.post(
        'http://localhost:5000/sessions',
        data={'email': EMAIL, 'password': NEW_PASSWD}
        )
    assert r.status_code == 401
    # assert AUTH.valid_login(EMAIL, NEW_PASSWD) is False


def profile_unlogged():
    '''Test profile of an unlogged user'''
    r = requests.get('http://127.0.0.1:5000/profile')
    assert r.status_code == 403


def log_in(EMAIL, PASSWD):
    '''Test log in'''
    r = requests.post(
        'http://127.0.0.1:5000/sessions',
        data={'email': EMAIL, 'password': PASSWD}
        )
    assert r.status_code == 200
    session_id = r.cookies.get('session_id')
    assert session_id is not None
    return session_id


def profile_logged(session_id):
    '''Test profile of a logged user'''
    cookies = dict(session_id=session_id)
    r = requests.get(
        'http://127.0.0.1:5000/profile',
        cookies=cookies
        )
    assert r.status_code != 403
    assert r.json()['email'] == AUTH.get_user_from_session_id(session_id).email


def log_out(session_id):
    '''Test log out'''
    r = requests.delete(
        'http://127.0.0.1:5000/sessions',
        cookies={'session_id': session_id}
        )
    assert r.status_code != 403
    # make sure the user is redirected to the welcome page
    assert r.history != []


def reset_password_token(EMAIL):
    '''Test reset password token'''
    r = requests.post(
        'http://localhost:5000/reset_password',
        data={'email': EMAIL}
        )
    assert r.status_code == 200
    assert r.json()['email'] == EMAIL
    reset_token = r.json()['reset_token']
    return reset_token


def update_password(EMAIL, reset_token, NEW_PASSWD):
    '''Test update password'''
    r = requests.put(
        'http://localhost:5000/reset_password',
        data={'email': EMAIL,
              'reset_token': reset_token,
              'new_password': NEW_PASSWD
              }
        )
    assert r.status_code == 200
    user = AUTH._db.find_user_by(email=EMAIL)
    assert user is not None
    assert bcrypt.checkpw(NEW_PASSWD.encode('utf-8'), user.hashed_password)


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
