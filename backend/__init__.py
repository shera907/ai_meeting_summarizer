"""
Backend initialization module
"""
from .app import app, socketio
from .config import Config
from .database import init_db, get_db_session
from .models import Meeting, ActionItem, Participant

__all__ = [
    'app',
    'socketio',
    'Config',
    'init_db',
    'get_db_session',
    'Meeting',
    'ActionItem',
    'Participant'
]

