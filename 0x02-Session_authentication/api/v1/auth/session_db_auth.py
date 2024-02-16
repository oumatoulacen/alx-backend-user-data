#!/usr/bin/env python3
''' Module for SessionDBAuth class'''
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from os import getenv
from typing import TypeVar
from datetime import datetime, timedelta
from uuid import uuid4


class SessionDBAuth(SessionExpAuth):
    ''' SessionDBAuth class'''
    def __init__(self):
        ''' Constructor'''
        self.session_duration = 0
        try:
            self.session_duration = int(getenv('SESSION_DURATION'))
        except Exception:
            pass

    def create_session(self, user_id: str = None) -> str:
        ''' Create a session ID'''
        if user_id is None:
            return None
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        ''' Return a User ID based on a Session ID'''
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None
        user_session = UserSession.search({'session_id': session_id})
        if user_session is None or not user_session:
            return None
        if self.session_duration <= 0:
            return user_session[0].user_id
        created_at = user_session[0].created_at
        if created_at is None:
            return None
        if (created_at + timedelta(seconds=self.session_duration)) \
                <= datetime.now():
            return None
        print('user_session[0].id', user_session[0].user_id)
        return user_session[0].user_id

    def destroy_session(self, request=None):
        ''' Delete the user session / log out'''
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_session = UserSession.search({'session_id': session_id})
        if user_session is None or not user_session:
            return False
        user_session[0].remove()
        return True
