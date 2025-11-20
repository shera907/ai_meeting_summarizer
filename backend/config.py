"""
Configuration settings for the application
"""
import os
from pathlib import Path


class Config:
    """Application configuration"""
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'true').lower() == 'true'
    
    # Database
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / 'data'
    DATABASE_PATH = os.getenv('DATABASE_PATH', str(DATA_DIR / 'meetings.db'))
    
    # AI Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
    DEEPGRAM_API_KEY = os.getenv('DEEPGRAM_API_KEY')
    ASSEMBLYAI_API_KEY = os.getenv('ASSEMBLYAI_API_KEY')
    
    # Euron.one API Configuration (Alternative OpenAI-compatible API)
    EURON_API_KEY = os.getenv('EURON_API_KEY')
    EURON_API_BASE = os.getenv('EURON_API_BASE', 'https://api.euron.one/api/v1/euri')
    EURON_MODEL = os.getenv('EURON_MODEL', 'gpt-4.1-mini')
    USE_EURON_API = os.getenv('USE_EURON_API', 'false').lower() == 'true'
    
    # Model Configuration
    USE_LOCAL_MODEL = os.getenv('USE_LOCAL_MODEL', 'false').lower() == 'true'
    LOCAL_MODEL_PATH = os.getenv('LOCAL_MODEL_PATH', './models/llama-2-7b-chat.gguf')
    TRANSCRIPTION_MODEL = os.getenv('TRANSCRIPTION_MODEL', 'whisper')
    
    # Audio settings
    AUDIO_DIR = DATA_DIR / 'audio'
    SAMPLE_RATE = 16000
    CHANNELS = 1
    
    # Integration APIs
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
    NOTION_API_KEY = os.getenv('NOTION_API_KEY')
    JIRA_API_URL = os.getenv('JIRA_API_URL')
    JIRA_API_TOKEN = os.getenv('JIRA_API_TOKEN')
    JIRA_EMAIL = os.getenv('JIRA_EMAIL')
    
    @classmethod
    def init_directories(cls):
        """Create necessary directories"""
        cls.DATA_DIR.mkdir(exist_ok=True)
        cls.AUDIO_DIR.mkdir(exist_ok=True)
        (cls.BASE_DIR / 'models').mkdir(exist_ok=True)


# Initialize directories
Config.init_directories()

