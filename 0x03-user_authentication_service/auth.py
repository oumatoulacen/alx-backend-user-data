#!/usr/bin/env python3
'''auth module.'''
import uuid
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    '''Hash a password.'''
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    '''Generate a UUID.'''
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self,
                      email: str,
                      password: str) -> User:
        '''Register a user.'''
        if not email or not password:
            return None
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError('User {} already exists.'.format(email))
        except NoResultFound:
            hashed_password = _hash_password(password)
            return self._db.add_user(email, hashed_password)

    def valid_login(self, email: str, password: str) -> bool:
        '''Validate login.'''
        if not email or not password:
            return False
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        '''Create a session.'''
        if not email:
            return None
        session_id = _generate_uuid()
        try:
            user = self._db.find_user_by(email=email)
            if not user:
                return None
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> str:
        '''Get a user from a session ID.'''
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None
