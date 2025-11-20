"""
Notion Export Agent
Exports meetings and action items to Notion
"""

import os
from datetime import datetime

# Notion SDK - optional import
try:
    from notion_client import Client
    NOTION_AVAILABLE = True
except ImportError:
    NOTION_AVAILABLE = False
    print("WARNING: Notion SDK not available. Install notion-client to enable export.")


class NotionExportAgent:
    """Exports meetings to Notion"""
    
    def __init__(self, api_key=None):
        self.client = None
        self.database_id = None
        
        if NOTION_AVAILABLE and api_key:
            try:
                self.client = Client(auth=api_key)
                print("Notion client initialized successfully")
            except Exception as e:
                print(f"Error initializing Notion client: {e}")
    
    def set_database(self, database_id):
        """Set the Notion database ID"""
        self.database_id = database_id
    
    def is_authenticated(self):
        """Check if Notion client is authenticated"""
        return self.client is not None
    
    def test_connection(self):
        """Test Notion API connection"""
        if not self.is_authenticated():
            raise Exception("Notion client not authenticated")
        
        try:
            # Try to list databases to verify connection
            self.client.search(filter={"property": "object", "value": "database"})
            return True
        except Exception as e:
            raise Exception(f"Notion connection test failed: {str(e)}")
    
    def export_meeting(self, meeting):
        """Export meeting to Notion page"""
        if not self.is_authenticated():
            raise Exception("Notion client not authenticated")
        
        if not self.database_id:
            # Create a new page in the workspace
            return self._create_standalone_page(meeting)
        else:
            # Add to existing database
            return self._add_to_database(meeting)
    
    def _create_standalone_page(self, meeting):
        """Create a standalone page for the meeting"""
        try:
            # Build action items text
            action_items_text = ""
            if meeting.action_items:
                action_items_text = "\n".join([
                    f"{'✅' if item.completed else '⬜'} {item.description} "
                    f"[{item.priority}]"
                    f"{' - ' + item.assignee if item.assignee else ''}"
                    for item in meeting.action_items
                ])
            else:
                action_items_text = "No action items"
            
            # Create page content
            page = self.client.pages.create(
                parent={"type": "page_id", "page_id": "workspace"},
                properties={
                    "title": {
                        "title": [
                            {
                                "text": {
                                    "content": meeting.title
                                }
                            }
                        ]
                    }
                },
                children=[
                    {
                        "object": "block",
                        "type": "heading_2",
                        "heading_2": {
                            "rich_text": [{"type": "text", "text": {"content": "Meeting Details"}}]
                        }
                    },
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {
                                        "content": f"Date: {meeting.start_time.strftime('%Y-%m-%d %H:%M') if meeting.start_time else 'N/A'}\n"
                                        f"Duration: {self._format_duration(meeting.start_time, meeting.end_time)}"
                                    }
                                }
                            ]
                        }
                    },
                    {
                        "object": "block",
                        "type": "heading_2",
                        "heading_2": {
                            "rich_text": [{"type": "text", "text": {"content": "Summary"}}]
                        }
                    },
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {"content": meeting.summary or "No summary available"}
                                }
                            ]
                        }
                    },
                    {
                        "object": "block",
                        "type": "heading_2",
                        "heading_2": {
                            "rich_text": [{"type": "text", "text": {"content": "Action Items"}}]
                        }
                    },
                    {
                        "object": "block",
                        "type": "to_do",
                        "to_do": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {"content": action_items_text}
                                }
                            ],
                            "checked": False
                        }
                    }
                ]
            )
            
            return page['id']
        
        except Exception as e:
            print(f"Error creating Notion page: {e}")
            raise
    
    def _add_to_database(self, meeting):
        """Add meeting to Notion database"""
        try:
            # Build action items as checkbox items
            action_items_blocks = []
            for item in meeting.action_items:
                action_items_blocks.append({
                    "object": "block",
                    "type": "to_do",
                    "to_do": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": f"{item.description} [{item.priority}]"
                                    f"{' - ' + item.assignee if item.assignee else ''}"
                                }
                            }
                        ],
                        "checked": item.completed
                    }
                })
            
            # Create database entry
            page = self.client.pages.create(
                parent={"database_id": self.database_id},
                properties={
                    "Name": {
                        "title": [
                            {
                                "text": {
                                    "content": meeting.title
                                }
                            }
                        ]
                    },
                    "Date": {
                        "date": {
                            "start": meeting.start_time.isoformat() if meeting.start_time else None
                        }
                    }
                },
                children=[
                    {
                        "object": "block",
                        "type": "heading_2",
                        "heading_2": {
                            "rich_text": [{"type": "text", "text": {"content": "Summary"}}]
                        }
                    },
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {"content": meeting.summary or "No summary"}
                                }
                            ]
                        }
                    },
                    {
                        "object": "block",
                        "type": "heading_2",
                        "heading_2": {
                            "rich_text": [{"type": "text", "text": {"content": "Action Items"}}]
                        }
                    },
                    *action_items_blocks
                ]
            )
            
            return page['id']
        
        except Exception as e:
            print(f"Error adding to Notion database: {e}")
            raise
    
    def _format_duration(self, start_time, end_time):
        """Format meeting duration"""
        if not start_time or not end_time:
            return "Unknown"
        
        duration = end_time - start_time
        minutes = int(duration.total_seconds() / 60)
        
        if minutes < 60:
            return f"{minutes} minutes"
        else:
            hours = minutes // 60
            mins = minutes % 60
            return f"{hours}h {mins}m"

