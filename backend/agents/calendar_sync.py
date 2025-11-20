"""
Google Calendar Sync Agent
Syncs action items to Google Calendar
"""

import os
import json
from datetime import datetime, timedelta
from pathlib import Path

# Google Calendar API - optional import
try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import Flow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    GOOGLE_AVAILABLE = True
except ImportError:
    GOOGLE_AVAILABLE = False
    print("WARNING: Google Calendar API not available. Install google-api-python-client to enable sync.")


class CalendarSyncAgent:
    """Syncs action items to Google Calendar"""
    
    def __init__(self):
        self.available = GOOGLE_AVAILABLE
        self.credentials = None
        self.service = None
        self.base_dir = Path(__file__).parent.parent.parent
        self.token_file = self.base_dir / 'data' / 'google_token.json'
        self.credentials_file = self.base_dir / 'data' / 'google_credentials.json'
        
        if GOOGLE_AVAILABLE:
            self._load_credentials()
        else:
            print("Google Calendar not available - feature disabled")
    
    def is_available(self):
        """Check if Google Calendar API is available"""
        return self.available
    
    def _load_credentials(self):
        """Load existing credentials if available"""
        if self.token_file.exists():
            try:
                self.credentials = Credentials.from_authorized_user_file(str(self.token_file))
                if self.credentials and self.credentials.valid:
                    self.service = build('calendar', 'v3', credentials=self.credentials)
                    print("Google Calendar credentials loaded successfully")
            except Exception as e:
                print(f"Error loading Google credentials: {e}")
    
    def is_authenticated(self):
        """Check if user is authenticated with Google"""
        return self.credentials is not None and self.credentials.valid
    
    def get_auth_url(self):
        """Get OAuth URL for user authentication"""
        if not self.available:
            raise Exception("Google Calendar API packages not installed. Run: pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib")
        
        if not self.credentials_file.exists():
            raise Exception("Google OAuth credentials file not found. Please add google_credentials.json to the data folder.")
        
        flow = Flow.from_client_secrets_file(
            str(self.credentials_file),
            scopes=['https://www.googleapis.com/auth/calendar.events'],
            redirect_uri='http://localhost:5000/api/google/callback'
        )
        
        auth_url, _ = flow.authorization_url(prompt='consent')
        return auth_url
    
    def complete_auth(self, code):
        """Complete OAuth flow with authorization code"""
        if not GOOGLE_AVAILABLE:
            raise Exception("Google Calendar API not installed")
        
        flow = Flow.from_client_secrets_file(
            str(self.credentials_file),
            scopes=['https://www.googleapis.com/auth/calendar.events'],
            redirect_uri='http://localhost:5000/api/google/callback'
        )
        
        flow.fetch_token(code=code)
        self.credentials = flow.credentials
        
        # Save credentials
        self.token_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.token_file, 'w') as f:
            f.write(self.credentials.to_json())
        
        self.service = build('calendar', 'v3', credentials=self.credentials)
        print("Google Calendar authentication successful")
    
    def sync_action_item(self, action_item):
        """Sync a single action item to Google Calendar"""
        if not self.is_authenticated():
            raise Exception("Not authenticated with Google Calendar")
        
        try:
            # Create event
            event_data = {
                'summary': action_item.description,
                'description': f'Action item from meeting\nPriority: {action_item.priority}',
                'start': {
                    'dateTime': self._format_datetime(action_item.due_date or datetime.now()),
                    'timeZone': 'UTC',
                },
                'end': {
                    'dateTime': self._format_datetime((action_item.due_date or datetime.now()) + timedelta(hours=1)),
                    'timeZone': 'UTC',
                },
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'popup', 'minutes': 30},
                    ],
                },
            }
            
            if action_item.external_id:
                # Update existing event
                event = self.service.events().update(
                    calendarId='primary',
                    eventId=action_item.external_id,
                    body=event_data
                ).execute()
            else:
                # Create new event
                event = self.service.events().insert(
                    calendarId='primary',
                    body=event_data
                ).execute()
            
            return event['id']
        
        except HttpError as e:
            print(f"Google Calendar API error: {e}")
            raise
    
    def delete_event(self, event_id):
        """Delete event from Google Calendar"""
        if not self.is_authenticated():
            raise Exception("Not authenticated with Google Calendar")
        
        try:
            self.service.events().delete(
                calendarId='primary',
                eventId=event_id
            ).execute()
        except HttpError as e:
            print(f"Error deleting calendar event: {e}")
    
    def _format_datetime(self, dt):
        """Format datetime for Google Calendar API"""
        if isinstance(dt, str):
            dt = datetime.fromisoformat(dt.replace('Z', '+00:00'))
        return dt.isoformat()

