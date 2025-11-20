"""
API endpoints for health check and system status
"""
from flask import jsonify
from backend.config import Config
from backend.agents.offline_processing import OfflineProcessingAgent
import sys
import os


def register_system_routes(app, offline_agent):
    """Register system-related routes"""
    
    @app.route('/api/system/status', methods=['GET'])
    def system_status():
        """Get system status and capabilities"""
        status = {
            'status': 'running',
            'version': '1.0.0',
            'python_version': sys.version,
            'config': {
                'transcription_model': Config.TRANSCRIPTION_MODEL,
                'use_local_model': Config.USE_LOCAL_MODEL,
                'database_path': Config.DATABASE_PATH,
            },
            'capabilities': offline_agent.check_offline_capabilities() if offline_agent else {},
            'integrations': {
                'google_calendar': bool(Config.GOOGLE_CLIENT_ID),
                'notion': bool(Config.NOTION_API_KEY),
                'jira': bool(Config.JIRA_API_URL and Config.JIRA_API_TOKEN),
            }
        }
        return jsonify(status)
    
    @app.route('/api/system/models', methods=['GET'])
    def model_info():
        """Get information about loaded AI models"""
        if offline_agent:
            return jsonify(offline_agent.get_model_info())
        return jsonify({'error': 'Offline agent not initialized'})

