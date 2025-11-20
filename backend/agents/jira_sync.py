"""
Jira Sync Agent
Syncs action items to Jira tasks
"""

import os

# Jira SDK - optional import
try:
    from jira import JIRA
    JIRA_AVAILABLE = True
except ImportError:
    JIRA_AVAILABLE = False
    print("WARNING: Jira SDK not available. Install jira to enable sync.")


class JiraSyncAgent:
    """Syncs action items to Jira"""
    
    def __init__(self):
        self.client = None
        self.project_key = None
    
    def configure(self, server_url, email, api_token, project_key):
        """Configure Jira connection"""
        if not JIRA_AVAILABLE:
            raise Exception("Jira SDK not installed")
        
        try:
            self.client = JIRA(
                server=server_url,
                basic_auth=(email, api_token)
            )
            self.project_key = project_key
            
            # Test connection
            self.client.myself()
            print(f"Jira client initialized successfully for project {project_key}")
        
        except Exception as e:
            print(f"Error initializing Jira client: {e}")
            raise
    
    def is_authenticated(self):
        """Check if Jira client is authenticated"""
        return self.client is not None
    
    def test_connection(self):
        """Test Jira connection"""
        if not self.is_authenticated():
            raise Exception("Jira client not authenticated")
        
        try:
            user = self.client.myself()
            return True
        except Exception as e:
            raise Exception(f"Jira connection test failed: {str(e)}")
    
    def sync_action_item(self, action_item):
        """Sync action item to Jira as a task"""
        if not self.is_authenticated():
            raise Exception("Jira client not authenticated")
        
        try:
            # Map priority
            jira_priority = self._map_priority(action_item.priority)
            
            # Build issue data
            issue_data = {
                'project': {'key': self.project_key},
                'summary': action_item.description,
                'description': f"Action item from meeting\nPriority: {action_item.priority}",
                'issuetype': {'name': 'Task'},
                'priority': {'name': jira_priority}
            }
            
            # Add assignee if available
            if action_item.assignee:
                # Try to find user by email or display name
                try:
                    users = self.client.search_users(action_item.assignee)
                    if users:
                        issue_data['assignee'] = {'accountId': users[0].accountId}
                except:
                    pass  # If user not found, skip assignee
            
            # Add due date if available
            if action_item.due_date:
                issue_data['duedate'] = action_item.due_date.strftime('%Y-%m-%d')
            
            if action_item.external_id:
                # Update existing issue
                issue = self.client.issue(action_item.external_id)
                issue.update(fields=issue_data)
            else:
                # Create new issue
                issue = self.client.create_issue(fields=issue_data)
            
            # Mark as done if completed
            if action_item.completed:
                try:
                    transitions = self.client.transitions(issue)
                    done_transition = next(
                        (t for t in transitions if 'done' in t['name'].lower()),
                        None
                    )
                    if done_transition:
                        self.client.transition_issue(issue, done_transition['id'])
                except:
                    pass  # If transition fails, skip
            
            return issue.key
        
        except Exception as e:
            print(f"Error syncing to Jira: {e}")
            raise
    
    def delete_issue(self, issue_key):
        """Delete issue from Jira"""
        if not self.is_authenticated():
            raise Exception("Jira client not authenticated")
        
        try:
            issue = self.client.issue(issue_key)
            issue.delete()
        except Exception as e:
            print(f"Error deleting Jira issue: {e}")
            raise
    
    def _map_priority(self, priority):
        """Map priority to Jira priority names"""
        priority_map = {
            'high': 'High',
            'medium': 'Medium',
            'low': 'Low'
        }
        return priority_map.get(priority.lower() if priority else '', 'Medium')

