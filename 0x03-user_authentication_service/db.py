#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a user to the database
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """Find a user by a given attribute
        """
        try:
            return self._session.query(User).filter_by(**kwargs).one()
        except NoResultFound as e:
            raise e
        except InvalidRequestError as e:
            raise e
        except Exception as e:
            raise e
        finally:
            self._session.close()

    def update_user(self, user_id, **kwargs) -> None:
        """Update a user
        """
        user = self.find_user_by(id=user_id)
        try:
            for key, value in kwargs.items():
                setattr(user, key, value)
        except ValueError as e:
            raise e
        finally:
            self._session.commit()
            self._session.close()
        return None
