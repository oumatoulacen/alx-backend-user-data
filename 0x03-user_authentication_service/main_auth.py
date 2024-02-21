#!/usr/bin/env python3
"""
Main file
"""
from auth import Auth
import bcrypt

# email = 'me@me.com'
# password = 'mySecuredPwd'

# auth = Auth()

# try:
#     user = auth.register_user(email, password)
#     print("successfully created a new user!")
# except ValueError as err:
#     print("could not create a new user: {}".format(err))

# try:
#     user = auth.register_user(email, password)
#     print("successfully created a new user!")
# except ValueError as err:
#     print("could not create a new user: {}".format(err))        


# print('----------------------------------------------------------------')

# credentials validation
email = 'bob@bob.com'
password = 'MyPwdOfBob'
auth = Auth()

auth.register_user(email, password)
user = auth._db.find_user_by(email=email)
print(bcrypt.checkpw(password.encode('utf-8'), user.hashed_password))
print(auth.valid_login(email, password))

print(auth.valid_login(email, "WrongPwd"))

print(auth.valid_login("unknown@email", password))


print('----------------------------------------------------------------')
# # 10- get session ID
# email = 'bob@bob.com'
# password = 'MyPwdOfBob'
# auth = Auth()

# auth.register_user(email, password)

# print(auth.create_session(email))
# print(auth.create_session("unknown@email.com"))


print('----------------------------------------------------------------')