# Create database setup using sqlalchemy here
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create engine
engine = create_engine('sqlite:///db.sqlite3', connect_args={'check_same_thread': False})
Base = declarative_base()

# Create a session
Session = sessionmaker(bind=engine)
db = Session()