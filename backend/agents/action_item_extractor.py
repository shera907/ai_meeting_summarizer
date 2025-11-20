"""
Action Item Extraction Agent
Extracts action items from meeting transcripts using LangGraph
"""
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from config import Config
from openai import OpenAI
import json
import re

# Optional: Only needed if using Claude API
try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    Anthropic = None


class ActionItemExtractorAgent:
    """Agent responsible for extracting action items from meetings"""
    
    def __init__(self):
        self.use_local = Config.USE_LOCAL_MODEL
        
        if not self.use_local:
            # Initialize OpenAI client (can be used for official OpenAI or Euron.one)
            if Config.USE_EURON_API and Config.EURON_API_KEY:
                # Use Euron.one API with OpenAI-compatible client
                self.openai_client = OpenAI(
                    api_key=Config.EURON_API_KEY,
                    base_url=Config.EURON_API_BASE
                )
                self.model_name = Config.EURON_MODEL
            elif Config.OPENAI_API_KEY:
                # Use official OpenAI API
                self.openai_client = OpenAI(api_key=Config.OPENAI_API_KEY)
                self.model_name = "gpt-4-turbo-preview"
            else:
                self.openai_client = None
                self.model_name = None
            
            # Optional: Anthropic/Claude support (only if installed)
            if ANTHROPIC_AVAILABLE and Config.ANTHROPIC_API_KEY:
                self.anthropic_client = Anthropic(api_key=Config.ANTHROPIC_API_KEY)
            else:
                self.anthropic_client = None
    
    def extract(self, transcript_data, summary=None) -> List[Dict]:
        """Extract action items from transcript and summary"""
        transcript_text = transcript_data.get('text', '') if isinstance(transcript_data, dict) else transcript_data
        
        prompt = self._create_extraction_prompt(transcript_text, summary)
        
        if self.openai_client:
            action_items = self._extract_openai(prompt)
        elif self.anthropic_client:
            action_items = self._extract_anthropic(prompt)
        else:
            action_items = self._extract_fallback(transcript_text)
        
        return action_items
    
    def _create_extraction_prompt(self, transcript, summary=None):
        """Create prompt for action item extraction"""
        context = f"Transcript:\n{transcript}"
        if summary:
            context += f"\n\nSummary:\n{summary}"
        
        return f"""You are an expert at identifying action items from meeting transcripts.

Analyze the following meeting content and extract ALL action items. For each action item, provide:
1. description: Clear description of what needs to be done
2. assignee: Who is responsible (if mentioned, otherwise null)
3. due_date: When it's due (if mentioned, otherwise null)
4. priority: Priority level (high, medium, or low)

Return your response as a JSON array of action items.

{context}

Example output format:
[
  {{
    "description": "Send project proposal to client",
    "assignee": "John Smith",
    "due_date": "2024-12-01",
    "priority": "high"
  }},
  {{
    "description": "Review Q4 budget report",
    "assignee": null,
    "due_date": null,
    "priority": "medium"
  }}
]

Action Items (JSON array):"""
    
    def _extract_openai(self, prompt) -> List[Dict]:
        """Extract action items using OpenAI API (official or Euron.one)"""
        try:
            response = self.openai_client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are an expert at extracting action items from meeting transcripts. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=2000
            )
            
            content = response.choices[0].message.content
            action_items = self._parse_action_items(content)
            return action_items
        
        except Exception as e:
            print(f"AI action item extraction error: {e}")
            return []
    
    def _extract_anthropic(self, prompt) -> List[Dict]:
        """Extract action items using Claude"""
        try:
            response = self.anthropic_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
                temperature=0.2,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            content = response.content[0].text
            action_items = self._parse_action_items(content)
            return action_items
        
        except Exception as e:
            print(f"Anthropic action item extraction error: {e}")
            return []
    
    def _parse_action_items(self, content: str) -> List[Dict]:
        """Parse action items from LLM response"""
        try:
            # Try to find JSON array in the response
            json_match = re.search(r'\[[\s\S]*\]', content)
            if json_match:
                json_str = json_match.group(0)
                action_items = json.loads(json_str)
                
                # Validate and normalize
                normalized_items = []
                for item in action_items:
                    normalized_item = {
                        'description': item.get('description', ''),
                        'assignee': item.get('assignee'),
                        'due_date': self._parse_due_date(item.get('due_date')),
                        'priority': item.get('priority', 'medium').lower()
                    }
                    if normalized_item['description']:
                        normalized_items.append(normalized_item)
                
                return normalized_items
            else:
                return []
        
        except json.JSONDecodeError as e:
            print(f"Error parsing action items JSON: {e}")
            return []
    
    def _parse_due_date(self, due_date_str):
        """Parse due date string"""
        if not due_date_str:
            return None
        
        try:
            # Try to parse ISO format
            return datetime.fromisoformat(due_date_str.replace('Z', '+00:00'))
        except:
            # Try common formats
            formats = ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y']
            for fmt in formats:
                try:
                    return datetime.strptime(due_date_str, fmt)
                except:
                    continue
        
        return None
    
    def _extract_fallback(self, transcript: str) -> List[Dict]:
        """Fallback extraction using keyword matching"""
        action_items = []
        
        # Look for action-oriented keywords
        action_keywords = [
            'will', 'should', 'need to', 'have to', 'must',
            'action item', 'todo', 'to do', 'task',
            'follow up', 'follow-up', 'next step'
        ]
        
        sentences = transcript.split('.')
        
        for sentence in sentences:
            sentence = sentence.strip()
            if any(keyword in sentence.lower() for keyword in action_keywords):
                action_items.append({
                    'description': sentence,
                    'assignee': None,
                    'due_date': None,
                    'priority': 'medium'
                })
        
        return action_items[:10]  # Limit to 10 items

