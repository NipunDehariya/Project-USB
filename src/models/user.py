from sqlalchemy import create_engine, Column, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import uuid

# Define the base class for the model
Base = declarative_base()

def generate_id():
    return str(uuid.uuid4())

# Define the User model
class User(Base):
    __tablename__ = 'users'

    id = Column("UserID", String, primary_key=True, default=generate_id)
    name = Column("FullName", String, nullable=False)
    username = Column("Username", String, unique=True)
    password = Column("Password", String)
    email = Column("Email", String)
    is_admin = Column("IsAdmin", Boolean, default=False)
    permitted = Column("Permitted", Boolean, default=False)
    permitted_from = Column("Per_from", DateTime, nullable=True)
    permitted_to = Column("Per_to", DateTime, nullable=True)
    latitude = Column("lat", String)
    longitude = Column("long", String)

    def __init__(self, name, username, password, email, is_admin, permitted, permitted_from, permitted_to, latitude, longitude):
        self.name = name
        self.username = username
        self.password = password
        self.email = email
        self.is_admin = is_admin
        self.permitted = permitted
        self.permitted_from = permitted_from
        self.permitted_to = permitted_to
        self.latitude = latitude
        self.longitude = longitude

    # Relationship to the Log model
    # logs = relationship("Log", back_populates="user") 

# Create an SQLite database
engine = create_engine('sqlite:///users.db')
Base.metadata.create_all(bind=engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Manually add users and admins
def add_user(name, username, password, email, is_admin, permitted, permitted_from, permitted_to, latitude, longitude):
    user = User(
        name=name,
        username=username,
        password=password,
        email = email,
        is_admin=is_admin,
        permitted=permitted,
        permitted_from=permitted_from,
        permitted_to=permitted_to,
        latitude=latitude,
        longitude=longitude
    )
    session.add(user)
    session.commit()
    print(f"User {name} added successfully.")

def delete_user(username):
    # Query the user by username
    user = session.query(User).filter_by(username=username).first()
    
    if user:
        # Delete the user
        session.delete(user)
        session.commit()
        print(f"User {username} deleted successfully.")
    else:
        print(f"User {username} not found.")

# Example usage: Deleting a user
# delete_user('user1')
# delete_user('user1')

# Example usage: Adding an Admin
# add_user(
#     name='Admin',
#     username='admin1',
#     password='admin123',
#     email='admin@email.com',
#     is_admin=True,
#     permitted=True,
#     permitted_from=datetime.now(),
#     permitted_to=datetime.now(),
#     latitude='23.457',
#     longitude='24.567'
# )
# add_user(
#     name='Aditya',
#     username='user2',
#     password='user123',
#     email='user@email.com',
#     is_admin=False,
#     permitted=False,
#     permitted_from=datetime.now(),
#     permitted_to=datetime.now(),
#     latitude='23.456',
#     longitude='24.567'
# )

