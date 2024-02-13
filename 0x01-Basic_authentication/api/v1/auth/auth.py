#!/usr/bin/env python3
""" Module of Auth views
"""
from typing import List, TypeVar
from flask import request, jsonify, abort


class Auth:
    """ Auth class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ require_auth method
        """
        return False

    def authorization_header(self, request=None) -> str:
        """ authorization_header method
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):  # type: ignore
        """ current_user method
        """
        return None
