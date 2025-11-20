"""
Database initialization and session management
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from config import Config

# Create base class for declarative models
Base = declarative_base()

# Create engine
engine = create_engine(f'sqlite:///{Config.DATABASE_PATH}', echo=Config.DEBUG)

# Create session factory
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


def init_db():
    """Initialize database and create all tables"""
    from models import Meeting, ActionItem, Participant
    Base.metadata.create_all(engine)
    print("Database initialized successfully")


def get_db_session():
    """Get database session"""
    return Session()


def close_db_session():
    """Close database session"""
    Session.remove()

