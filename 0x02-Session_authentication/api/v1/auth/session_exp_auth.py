#!/usr/bin/env python3
''' Module for SessionExpAuth class'''
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta
from typing import TypeVar

from models.user import User


class SessionExpAuth(SessionAuth):
    ''' SessionExpAuth class'''
    def __init__(self):
        ''' Constructor'''
        self.session_duration = int(getenv('SESSION_DURATION', 0))

    def create_session(self, user_id: str = None) -> str:
        ''' Create a session ID'''
        if user_id is None:
            print('id is none')
            return None
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {'user_id': user_id, 'created_at': datetime.now()}
        self.user_id_by_session_id[session_id] = session_dictionary
        print('session_created:', self.user_id_by_session_id)
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        ''' Return a User ID based on a Session ID'''
        if session_id is None:
            print('session_id1:', session_id)
            return None
        if not isinstance(session_id, str):
            print('session_id2:', session_id)
            return None
        session_dictionary = self.user_id_by_session_id.get(session_id)
        if session_dictionary is None:
            print('session_id2:', session_id)
            return None
        if self.session_duration <= 0:
            print('session_id4:', session_id)
            return session_dictionary.get('user_id')
        if 'created_at' not in session_dictionary:
            print('session_id5:', session_id)
            return None
        created_at = session_dictionary.get('created_at')
        if created_at is None:
            print('session_id6:', session_id)
            return None
        if (created_at + timedelta(seconds=self.session_duration)) \
                < datetime.now():
            print('session_id7:', session_id)
            return None
        print('session_id8:', session_id)
        return session_dictionary.get('user_id')
