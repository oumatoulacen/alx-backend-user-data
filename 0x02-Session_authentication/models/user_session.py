#!/usr/bin/env python3
""" UserSession module
"""
import hashlib
from models.base import Base


class UserSession(Base):
    """ UserSession class
    """
    def __init__(self, *args: list, **kwargs: dict):
        """ Constructor
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')

    def __str__(self) -> str:
        """ String representation
        """
        return str(self.user_id) + ' ' + str(self.session_id)

    def save(self) -> None:
        """ Save method
        """
        self.session_id = self._generate_uuid()
        super().save()

    def _generate_uuid(self) -> str:
        """ Generate a UUID
        """
        return str(hashlib.md5(str(self.user_id).encode()).hexdigest())