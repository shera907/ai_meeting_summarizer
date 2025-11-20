"""
Database models for the AI Meeting Summarizer
"""
import json
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Meeting(Base):
    """Meeting model"""
    __tablename__ = 'meetings'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    transcript = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    audio_file_path = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    action_items = relationship('ActionItem', back_populates='meeting', cascade='all, delete-orphan')
    participants = relationship('Participant', back_populates='meeting', cascade='all, delete-orphan')
    
    def end_meeting(self):
        """Mark meeting as ended"""
        self.end_time = datetime.utcnow()
    
    def to_dict(self):
        """Convert to dictionary"""
        # Parse transcript from JSON string if needed
        transcript = self.transcript
        if transcript and isinstance(transcript, str):
            try:
                transcript = json.loads(transcript)
            except (json.JSONDecodeError, ValueError):
                # If it's not valid JSON, keep it as string
                pass
        
        return {
            'id': self.id,
            'title': self.title,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'transcript': transcript,
            'summary': self.summary,
            'audio_file_path': self.audio_file_path,
            'action_items': [item.to_dict() for item in self.action_items],
            'participants': [p.to_dict() for p in self.participants],
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class ActionItem(Base):
    """Action Item model"""
    __tablename__ = 'action_items'
    
    id = Column(Integer, primary_key=True)
    meeting_id = Column(Integer, ForeignKey('meetings.id'), nullable=False)
    description = Column(Text, nullable=False)
    assignee = Column(String(255), nullable=True)
    due_date = Column(DateTime, nullable=True)
    priority = Column(String(50), default='medium')  # low, medium, high
    completed = Column(Boolean, default=False)
    synced_to_calendar = Column(Boolean, default=False)
    synced_to_notion = Column(Boolean, default=False)
    synced_to_jira = Column(Boolean, default=False)
    external_id = Column(String(255), nullable=True)  # ID from external service
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    meeting = relationship('Meeting', back_populates='action_items')
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'meeting_id': self.meeting_id,
            'description': self.description,
            'assignee': self.assignee,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'priority': self.priority,
            'completed': self.completed,
            'synced_to_calendar': self.synced_to_calendar,
            'synced_to_notion': self.synced_to_notion,
            'synced_to_jira': self.synced_to_jira,
            'external_id': self.external_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Participant(Base):
    """Meeting Participant model"""
    __tablename__ = 'participants'
    
    id = Column(Integer, primary_key=True)
    meeting_id = Column(Integer, ForeignKey('meetings.id'), nullable=False)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True)
    role = Column(String(100), nullable=True)
    
    # Relationships
    meeting = relationship('Meeting', back_populates='participants')
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'meeting_id': self.meeting_id,
            'name': self.name,
            'email': self.email,
            'role': self.role
        }

