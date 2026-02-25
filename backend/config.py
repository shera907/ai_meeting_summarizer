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
    SAMPLE_RATE = int(os.getenv('AUDIO_SAMPLE_RATE', '16000'))
    CHANNELS = int(os.getenv('AUDIO_CHANNELS', '1'))
    
    # ========================================
    # GOOGLE CALENDAR INTEGRATION
    # ========================================
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
    GOOGLE_CALENDAR_ENABLED = os.getenv('GOOGLE_CALENDAR_ENABLED', 'false').lower() == 'true'
    GOOGLE_CALENDAR_NAME = os.getenv('GOOGLE_CALENDAR_NAME', 'AI Meeting Summarizer')
    GOOGLE_DEFAULT_REMINDER_MINUTES = int(os.getenv('GOOGLE_DEFAULT_REMINDER_MINUTES', '30'))
    GOOGLE_CREATE_ALL_DAY_EVENTS = os.getenv('GOOGLE_CREATE_ALL_DAY_EVENTS', 'false').lower() == 'true'
    
    # ========================================
    # NOTION INTEGRATION
    # ========================================
    NOTION_API_KEY = os.getenv('NOTION_API_KEY')
    NOTION_DATABASE_ID = os.getenv('NOTION_DATABASE_ID')
    NOTION_ENABLED = os.getenv('NOTION_ENABLED', 'false').lower() == 'true'
    NOTION_PAGE_ICON = os.getenv('NOTION_PAGE_ICON', '🎙️')
    NOTION_AUTO_SYNC = os.getenv('NOTION_AUTO_SYNC', 'true').lower() == 'true'
    NOTION_CREATE_TASKS_DATABASE = os.getenv('NOTION_CREATE_TASKS_DATABASE', 'true').lower() == 'true'
    NOTION_WORKSPACE_ID = os.getenv('NOTION_WORKSPACE_ID')
    
    # ========================================
    # JIRA INTEGRATION
    # ========================================
    JIRA_ENABLED = os.getenv('JIRA_ENABLED', 'false').lower() == 'true'
    JIRA_API_URL = os.getenv('JIRA_API_URL')
    JIRA_EMAIL = os.getenv('JIRA_EMAIL')
    JIRA_API_TOKEN = os.getenv('JIRA_API_TOKEN')
    JIRA_PROJECT_KEY = os.getenv('JIRA_PROJECT_KEY')
    JIRA_DEFAULT_ISSUE_TYPE = os.getenv('JIRA_DEFAULT_ISSUE_TYPE', 'Task')
    JIRA_DEFAULT_PRIORITY = os.getenv('JIRA_DEFAULT_PRIORITY', 'Medium')
    JIRA_AUTO_ASSIGN = os.getenv('JIRA_AUTO_ASSIGN', 'false').lower() == 'true'
    JIRA_ADD_MEETING_LINK = os.getenv('JIRA_ADD_MEETING_LINK', 'true').lower() == 'true'
    JIRA_LABEL_PREFIX = os.getenv('JIRA_LABEL_PREFIX', 'meeting-')
    JIRA_PRIORITY_HIGH = os.getenv('JIRA_PRIORITY_HIGH', 'High')
    JIRA_PRIORITY_MEDIUM = os.getenv('JIRA_PRIORITY_MEDIUM', 'Medium')
    JIRA_PRIORITY_LOW = os.getenv('JIRA_PRIORITY_LOW', 'Low')
    
    # ========================================
    # SLACK INTEGRATION (Future)
    # ========================================
    SLACK_ENABLED = os.getenv('SLACK_ENABLED', 'false').lower() == 'true'
    SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')
    SLACK_CHANNEL_ID = os.getenv('SLACK_CHANNEL_ID')
    SLACK_WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_URL')
    
    # ========================================
    # MICROSOFT TEAMS INTEGRATION (Future)
    # ========================================
    TEAMS_ENABLED = os.getenv('TEAMS_ENABLED', 'false').lower() == 'true'
    TEAMS_WEBHOOK_URL = os.getenv('TEAMS_WEBHOOK_URL')
    TEAMS_CHANNEL_ID = os.getenv('TEAMS_CHANNEL_ID')
    
    # ========================================
    # EMAIL INTEGRATION (Future)
    # ========================================
    EMAIL_ENABLED = os.getenv('EMAIL_ENABLED', 'false').lower() == 'true'
    SMTP_HOST = os.getenv('SMTP_HOST', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
    SMTP_USERNAME = os.getenv('SMTP_USERNAME')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
    EMAIL_FROM_ADDRESS = os.getenv('EMAIL_FROM_ADDRESS')
    EMAIL_AUTO_SEND = os.getenv('EMAIL_AUTO_SEND', 'false').lower() == 'true'
    
    # ========================================
    # ADVANCED SETTINGS
    # ========================================
    # Audio Settings
    AUDIO_SAMPLE_RATE = int(os.getenv('AUDIO_SAMPLE_RATE', '16000'))
    AUDIO_CHANNELS = int(os.getenv('AUDIO_CHANNELS', '1'))
    AUDIO_FORMAT = os.getenv('AUDIO_FORMAT', 'wav')
    MAX_AUDIO_DURATION_MINUTES = int(os.getenv('MAX_AUDIO_DURATION_MINUTES', '120'))
    
    # Transcription Settings
    LIVE_TRANSCRIPTION_INTERVAL = int(os.getenv('LIVE_TRANSCRIPTION_INTERVAL', '10'))
    TRANSCRIPTION_LANGUAGE = os.getenv('TRANSCRIPTION_LANGUAGE', 'en')
    ENABLE_SPEAKER_DIARIZATION = os.getenv('ENABLE_SPEAKER_DIARIZATION', 'false').lower() == 'true'
    
    # AI Processing Settings
    MAX_SUMMARY_LENGTH = int(os.getenv('MAX_SUMMARY_LENGTH', '500'))
    MIN_ACTION_ITEM_CONFIDENCE = float(os.getenv('MIN_ACTION_ITEM_CONFIDENCE', '0.7'))
    ENABLE_AUTO_TRANSLATION = os.getenv('ENABLE_AUTO_TRANSLATION', 'false').lower() == 'true'
    DEFAULT_TRANSLATION_LANGUAGE = os.getenv('DEFAULT_TRANSLATION_LANGUAGE', 'en')
    
    # Security Settings
    ENABLE_ENCRYPTION = os.getenv('ENABLE_ENCRYPTION', 'false').lower() == 'true'
    ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY')
    SESSION_TIMEOUT_MINUTES = int(os.getenv('SESSION_TIMEOUT_MINUTES', '60'))
    MAX_FILE_SIZE_MB = int(os.getenv('MAX_FILE_SIZE_MB', '100'))
    
    # Performance Settings
    ENABLE_CACHING = os.getenv('ENABLE_CACHING', 'true').lower() == 'true'
    CACHE_DURATION_HOURS = int(os.getenv('CACHE_DURATION_HOURS', '24'))
    MAX_CONCURRENT_PROCESSING = int(os.getenv('MAX_CONCURRENT_PROCESSING', '3'))
    ENABLE_GPU_ACCELERATION = os.getenv('ENABLE_GPU_ACCELERATION', 'false').lower() == 'true'
    
    # Backup and Storage
    AUTO_BACKUP_ENABLED = os.getenv('AUTO_BACKUP_ENABLED', 'false').lower() == 'true'
    BACKUP_DIRECTORY = os.getenv('BACKUP_DIRECTORY', 'backups/')
    BACKUP_FREQUENCY_HOURS = int(os.getenv('BACKUP_FREQUENCY_HOURS', '24'))
    KEEP_BACKUPS_DAYS = int(os.getenv('KEEP_BACKUPS_DAYS', '30'))
    CLOUD_STORAGE_ENABLED = os.getenv('CLOUD_STORAGE_ENABLED', 'false').lower() == 'true'
    CLOUD_STORAGE_PROVIDER = os.getenv('CLOUD_STORAGE_PROVIDER')
    CLOUD_STORAGE_BUCKET = os.getenv('CLOUD_STORAGE_BUCKET')
    
    @classmethod
    def init_directories(cls):
        """Create necessary directories"""
        cls.DATA_DIR.mkdir(exist_ok=True)
        cls.AUDIO_DIR.mkdir(exist_ok=True)
        (cls.BASE_DIR / 'models').mkdir(exist_ok=True)


# Initialize directories
Config.init_directories()

