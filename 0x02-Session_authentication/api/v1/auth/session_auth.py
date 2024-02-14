#!/usr/bin/env python3
''' Module for SessionAuth class'''
from typing import List, Tuple, TypeVar
from flask import request, jsonify, abort
import base64
from api.v1.auth.auth import Auth
from models.user import User
from uuid import uuid4


class SessionAuth(Auth):
    ''' Auth class for session'''
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        ''' Create a session ID'''
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        else:
            session_id = str(uuid4())
            self.user_id_by_session_id[session_id] = user_id
            return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        ''' Return a User ID based on a Session ID'''
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)
