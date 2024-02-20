from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, select

# Define a metadata
metadata = MetaData()

# Define a table
users = Table('users',
              metadata,
              Column('id',Integer, primary_key=True),
              Column('name', String(50)),
              Column('email', String(50))
              )

engine = create_engine('sqlite:///core_example.db', echo=True)
metadata.create_all(engine)

conn = engine.connect()

# insert data
# ins1 = users.insert().values(name='John Doe', email='johndoe@example.com')
# ins2 = users.insert().values(name='missive', email='missive@example.com')
# ins3 = users.insert().values(name='jane', email='jane@gmail.com')

# conn.execute(ins1)
# conn.execute(ins2)
# conn.execute(ins3)

# commit the changes
# conn.commit()

# Selecting data
stmt = select(users)
result = conn.execute(stmt)
for row in result:
    print(row)


conn.close()