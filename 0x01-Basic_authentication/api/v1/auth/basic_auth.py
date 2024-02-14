#!/usr/bin/env python3
''' Module of Auth views'''
from typing import List, Tuple, TypeVar
from flask import request, jsonify, abort
import base64
from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    '''basic auth class'''
    def extract_base64_authorization_header(self,
                                            authorization_header: str
                                            ) -> str:
        '''return the Base64 part of the Authorization header'''
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        '''return the decoded of a Base64 string base64_authorization_header'''
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            return base64.b64decode(
                base64_authorization_header).decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> Tuple[str, str]:
        '''return the user email and password from the Base64 decoded value'''
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        return tuple(decoded_base64_authorization_header.split(':', 1))

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        '''return the User instance based on his email and password'''
        if user_email is None or not user_email:
            return None
        if user_pwd is None or not user_pwd:
            return None
        try:
            user = User.search({'email': user_email})[0]
            if user is None:
                return None
            if user.is_valid_password(user_pwd):
                return user
            else:
                return None
        except Exception:
            return None
