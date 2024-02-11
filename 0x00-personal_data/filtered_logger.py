#!/usr/bin/env python3
'''implements a filter_datum that returns the log message obfuscated:
'''
import re
from typing import List
import logging
import os
import mysql.connector


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    '''returns the log message obfuscated'''
    for field in fields:
        message = re.sub(rf'{field}=.+?{separator}',
                         f'{field}={redaction}{separator}', message)
    return message


# def get_logger() -> logging.Logger:
#     '''returns a logging object'''
#     logger = logging.getLogger('user_data')
#     logger.setLevel(logging.INFO)
#     logger.propagate = False
#     stream_handler = logging.StreamHandler()
#     formatter = RedactingFormatter(list(PII_FIELDS))
#     stream_handler.setFormatter(formatter)
#     logger.addHandler(stream_handler)
#     return logger


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class that
    redacts sensitive data in log messages."""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record and redact sensitive data.
        """
        message = super(RedactingFormatter, self).format(record)
        return filter_datum(self.fields, self.REDACTION,
                            message, self.SEPARATOR)


# containing the fields from user_data.csv that are considered PII.
PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def get_logger() -> logging.Logger:
    ''' returns a logging.Logger object'''
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(list(PII_FIELDS))
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    '''Returns a connector to the database.'''

    user: str = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password: str = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host: str = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db: str = os.getenv('PERSONAL_DATA_DB_NAME')
    con: mysql.connector.connection.MySQLConnection = (
        mysql.connector.connection.MySQLConnection(
            user=user,
            password=password,
            host=host,
            database=db
        )
    )
    return con
