#!/usr/bin/env python3
''' Module of Auth views'''
from typing import List, TypeVar
from flask import request, jsonify, abort
import base64
from api.v1.auth.auth import Auth


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
