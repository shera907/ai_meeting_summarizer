"""
Offline Processing Agent
Handles local model initialization and offline operations
"""
import os
from pathlib import Path
from config import Config


class OfflineProcessingAgent:
    """Agent responsible for offline/local AI processing"""
    
    def __init__(self):
        self.local_llm = None
        self.whisper_model = None
        self.is_offline_ready = False
        
        if Config.USE_LOCAL_MODEL:
            self._init_offline_mode()
    
    def _init_offline_mode(self):
        """Initialize offline processing capabilities"""
        try:
            # Initialize local LLM
            if os.path.exists(Config.LOCAL_MODEL_PATH):
                from llama_cpp import Llama
                self.local_llm = Llama(
                    model_path=Config.LOCAL_MODEL_PATH,
                    n_ctx=4096,
                    n_threads=4
                )
                print("✓ Local LLM loaded successfully")
            else:
                print(f"⚠ Local model not found at {Config.LOCAL_MODEL_PATH}")
            
            # Initialize Whisper
            import whisper
            self.whisper_model = whisper.load_model("base")
            print("✓ Whisper model loaded successfully")
            
            self.is_offline_ready = True
            print("✓ Offline mode is ready")
        
        except Exception as e:
            print(f"✗ Error initializing offline mode: {e}")
            print("Falling back to online APIs")
            self.is_offline_ready = False
    
    def check_offline_capabilities(self):
        """Check if offline processing is available"""
        return {
            'offline_ready': self.is_offline_ready,
            'local_llm_available': self.local_llm is not None,
            'whisper_available': self.whisper_model is not None,
            'transcription_mode': Config.TRANSCRIPTION_MODEL,
            'use_local_model': Config.USE_LOCAL_MODEL
        }
    
    def transcribe_offline(self, audio_file):
        """Transcribe audio using local Whisper model"""
        if not self.whisper_model:
            raise RuntimeError("Whisper model not initialized")
        
        result = self.whisper_model.transcribe(audio_file)
        return {
            'text': result['text'],
            'segments': result.get('segments', []),
            'language': result.get('language', 'en')
        }
    
    def summarize_offline(self, transcript):
        """Summarize using local LLM"""
        if not self.local_llm:
            raise RuntimeError("Local LLM not initialized")
        
        prompt = f"""Summarize the following meeting transcript concisely.

Transcript:
{transcript}

Summary:"""
        
        response = self.local_llm(
            prompt,
            max_tokens=500,
            temperature=0.3,
            stop=["Transcript:", "User:"]
        )
        
        return response['choices'][0]['text'].strip()
    
    def extract_actions_offline(self, transcript):
        """Extract action items using local LLM"""
        if not self.local_llm:
            raise RuntimeError("Local LLM not initialized")
        
        prompt = f"""Extract action items from this meeting transcript. List each action item on a new line starting with "- ".

Transcript:
{transcript}

Action Items:"""
        
        response = self.local_llm(
            prompt,
            max_tokens=300,
            temperature=0.2,
            stop=["Transcript:", "User:"]
        )
        
        # Parse response
        action_text = response['choices'][0]['text'].strip()
        action_items = []
        
        for line in action_text.split('\n'):
            line = line.strip()
            if line.startswith('- ') or line.startswith('• '):
                description = line[2:].strip()
                if description:
                    action_items.append({
                        'description': description,
                        'assignee': None,
                        'due_date': None,
                        'priority': 'medium'
                    })
        
        return action_items
    
    def get_model_info(self):
        """Get information about loaded models"""
        return {
            'local_llm': {
                'loaded': self.local_llm is not None,
                'path': Config.LOCAL_MODEL_PATH if self.local_llm else None
            },
            'whisper': {
                'loaded': self.whisper_model is not None,
                'model': 'base' if self.whisper_model else None
            }
        }

