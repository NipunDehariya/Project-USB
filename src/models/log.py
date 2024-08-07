from sqlalchemy import create_engine, Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime, timezone
from user import User  

# Define the base class for the model
Base = declarative_base()

# Define the Log model
class Log(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    logged_in = Column(DateTime)
    logged_out = Column(DateTime, nullable=True)
    session_duration = Column(Integer, nullable=True)  # Duration in seconds

    # Relationship to the User model
    user = relationship("User", back_populates="logs")

# Create an SQLite database
engine = create_engine('sqlite:///logs.db')
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Example usage: Logging user activity
def log_user_activity(user_id, logged_out=None):
    log_entry = session.query(Log).filter_by(user_id=user_id).order_by(Log.logged_in.desc()).first()
    if log_entry and not log_entry.logged_out:
        log_entry.logged_out = logged_out or datetime.now(timezone.utc)
        log_entry.session_duration = (log_entry.logged_out - log_entry.logged_in).total_seconds()
    else:
        log_entry = Log(user_id=user_id, logged_in=datetime.now(timezone.utc))
        session.add(log_entry)
    session.commit()

# Example usage: Logging in a user
log_user_activity(user_id='1')

# Example usage: Logging out a user
log_user_activity(user_id='1', logged_out=datetime.now(timezone.utc))