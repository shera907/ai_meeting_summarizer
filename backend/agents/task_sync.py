"""
Task Sync Agent
Syncs action items to external services (Google Calendar, Notion, Jira)
"""
from datetime import datetime, timedelta
from typing import List, Dict
from config import Config
import json


class TaskSyncAgent:
    """Agent responsible for syncing action items to external services"""
    
    def __init__(self):
        self.google_client = None
        self.notion_client = None
        self.jira_client = None
        
        self._init_clients()
    
    def _init_clients(self):
        """Initialize API clients"""
        # Google Calendar
        if Config.GOOGLE_CLIENT_ID and Config.GOOGLE_CLIENT_SECRET:
            try:
                from google.oauth2.credentials import Credentials
                from googleapiclient.discovery import build
                # Note: In production, implement proper OAuth flow
                print("Google Calendar client initialized (OAuth required)")
            except Exception as e:
                print(f"Google Calendar initialization error: {e}")
        
        # Notion
        if Config.NOTION_API_KEY:
            try:
                from notion_client import Client
                self.notion_client = Client(auth=Config.NOTION_API_KEY)
                print("Notion client initialized")
            except Exception as e:
                print(f"Notion initialization error: {e}")
        
        # Jira
        if Config.JIRA_API_URL and Config.JIRA_API_TOKEN:
            try:
                from jira import JIRA
                self.jira_client = JIRA(
                    server=Config.JIRA_API_URL,
                    basic_auth=(Config.JIRA_EMAIL, Config.JIRA_API_TOKEN)
                )
                print("Jira client initialized")
            except Exception as e:
                print(f"Jira initialization error: {e}")
    
    def sync_tasks(self, meeting, action_items, services: List[str]) -> Dict:
        """Sync action items to specified services"""
        results = {
            'google_calendar': {'success': False, 'synced': 0, 'error': None},
            'notion': {'success': False, 'synced': 0, 'error': None},
            'jira': {'success': False, 'synced': 0, 'error': None}
        }
        
        for service in services:
            if service == 'google_calendar':
                results['google_calendar'] = self._sync_to_google_calendar(meeting, action_items)
            elif service == 'notion':
                results['notion'] = self._sync_to_notion(meeting, action_items)
            elif service == 'jira':
                results['jira'] = self._sync_to_jira(meeting, action_items)
        
        return results
    
    def _sync_to_google_calendar(self, meeting, action_items) -> Dict:
        """Sync action items to Google Calendar"""
        try:
            if not self.google_client:
                return {
                    'success': False,
                    'synced': 0,
                    'error': 'Google Calendar not configured'
                }
            
            # Implementation requires OAuth flow
            # For now, return placeholder
            return {
                'success': False,
                'synced': 0,
                'error': 'OAuth flow required - see documentation'
            }
        
        except Exception as e:
            return {
                'success': False,
                'synced': 0,
                'error': str(e)
            }
    
    def _sync_to_notion(self, meeting, action_items) -> Dict:
        """Sync action items to Notion"""
        try:
            if not self.notion_client:
                return {
                    'success': False,
                    'synced': 0,
                    'error': 'Notion not configured'
                }
            
            # Note: Requires a database ID to be configured
            # This is a simplified implementation
            synced_count = 0
            
            for item in action_items:
                # Create page in Notion database
                # Note: You need to create a database in Notion first and get its ID
                # Then configure it in the application
                
                page_data = {
                    "parent": {"database_id": "YOUR_NOTION_DATABASE_ID"},
                    "properties": {
                        "Name": {
                            "title": [
                                {
                                    "text": {
                                        "content": item.description
                                    }
                                }
                            ]
                        },
                        "Status": {
                            "select": {
                                "name": "To Do"
                            }
                        },
                        "Priority": {
                            "select": {
                                "name": item.priority.capitalize()
                            }
                        }
                    }
                }
                
                # Uncomment when database ID is configured
                # self.notion_client.pages.create(**page_data)
                # synced_count += 1
            
            return {
                'success': False,
                'synced': 0,
                'error': 'Notion database ID required - see documentation'
            }
        
        except Exception as e:
            return {
                'success': False,
                'synced': 0,
                'error': str(e)
            }
    
    def _sync_to_jira(self, meeting, action_items) -> Dict:
        """Sync action items to Jira"""
        try:
            if not self.jira_client:
                return {
                    'success': False,
                    'synced': 0,
                    'error': 'Jira not configured'
                }
            
            synced_count = 0
            
            for item in action_items:
                # Create Jira issue
                issue_dict = {
                    'project': {'key': 'PROJ'},  # Configure your project key
                    'summary': item.description,
                    'description': f"Action item from meeting: {meeting.title}",
                    'issuetype': {'name': 'Task'},
                    'priority': {'name': self._map_priority_to_jira(item.priority)}
                }
                
                if item.assignee:
                    # Note: Assignee must be a valid Jira user
                    issue_dict['assignee'] = {'name': item.assignee}
                
                if item.due_date:
                    issue_dict['duedate'] = item.due_date.strftime('%Y-%m-%d')
                
                # Uncomment when Jira is properly configured
                # new_issue = self.jira_client.create_issue(fields=issue_dict)
                # synced_count += 1
            
            return {
                'success': False,
                'synced': 0,
                'error': 'Jira project key required - see documentation'
            }
        
        except Exception as e:
            return {
                'success': False,
                'synced': 0,
                'error': str(e)
            }
    
    def _map_priority_to_jira(self, priority: str) -> str:
        """Map internal priority to Jira priority"""
        priority_map = {
            'low': 'Low',
            'medium': 'Medium',
            'high': 'High',
            'urgent': 'Highest'
        }
        return priority_map.get(priority.lower(), 'Medium')

