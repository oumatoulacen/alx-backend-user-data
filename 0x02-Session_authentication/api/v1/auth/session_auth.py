#!/usr/bin/env python3
''' Module for SessionAuth class'''
from typing import List, Tuple, TypeVar
from flask import request, jsonify, abort
import base64
from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    ''' Auth class for session'''
    pass
