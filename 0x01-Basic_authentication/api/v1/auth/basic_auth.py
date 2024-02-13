#!/usr/bin/env python3
''' Module of Auth views'''
from typing import List, TypeVar
from flask import request, jsonify, abort

from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    '''basic auth class'''
    pass
