from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    email = Column(String(200))

# Connect to the database
engine = create_engine('sqlite:///orm_example.db')

# Create tables
# Base.metadata.create_all(engine)


# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# # Insert data
# session.add_all([
#     User(name='Alice', email='alice@example.com'),
#     User(name='Bob', email='bob@example.com'),
#     User(name='Charlie', email='charlie@example.com')
# ])

# # Commit the changes
# session.commit()

# Query all users
users = session.query(User).all()

# Print the users
for user in users:
    print(user.id, user.name, user.email)

# Close the session
session.close()