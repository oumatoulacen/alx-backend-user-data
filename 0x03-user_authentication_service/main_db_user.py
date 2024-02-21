#!/usr/bin/env python3
"""
Main file
"""
from user import User
from db import DB
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

my_db = DB()

# 0. User model
# print(User.__tablename__)
# for column in User.__table__.columns:
#     print("{}: {}".format(column, column.type))


# 1. create user
# user_1 = my_db.add_user("test@test.com", "SuperHashedPwd")
# print(user_1.id)

# user_2 = my_db.add_user("test1@test.com", "SuperHashedPwd1")
# print(user_2.id) 

# 2. find user
# user = my_db.add_user("test@test.com", "PwdHashed")
# print(user.id)

# find_user = my_db.find_user_by(email="test@test.com")
# print(find_user.id)

# try:
#     find_user = my_db.find_user_by(email="test2@test.com")
#     print(find_user.id)
# except NoResultFound:
#     print("Not found")

# try:
#     find_user = my_db.find_user_by(no_email="test@test.com")
#     print(find_user.id)
# except InvalidRequestError:
#     print("Invalid")

# 3. update user
# email = 'test@test.com'
# hashed_password = "hashedPwd"

# user = my_db.add_user(email, hashed_password)
# print(user.id)

# try:
#     my_db.update_user(user.id, hashed_password='NewPwd')
#     print("Password updated")
# except ValueError:
#     print("Error")

# res = my_db.find_user_by(email=email) 
# print(res.hashed_password)


# 4. Hash password

from auth import _hash_password
print(_hash_password("Hello Holberton"))
