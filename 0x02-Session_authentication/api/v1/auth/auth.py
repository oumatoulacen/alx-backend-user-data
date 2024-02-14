#!/usr/bin/env python3
""" Module of Auth views
"""
from typing import List, TypeVar
from flask import request, jsonify, abort
from os import getenv


class Auth:
    """ Auth class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """return True if the path is not in the list of strings excluded_paths
        """
        if (path is None or excluded_paths is None
                or excluded_paths == []):
            return True
        if (path[-1] != '/' and path + '/' in excluded_paths or
                path in excluded_paths):
            return False
        for p in excluded_paths:
            if p[-1] == '*' and path.startswith(p[:-1]):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """ eturn the value of the header request Authorization
        """
        if request is None:
            return None
        if request.headers.get('Authorization') is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):  # type: ignore
        """ current_user method
        """
        return None

    def session_cookie(self, request=None):
        ''' returns a cookie value from a request'''
        _my_session_id = getenv('SESSION_NAME')
        if request is None:
            return None
        return request.cookies.get(_my_session_id)
