"""
AI Meeting Summarizer - Flask Backend
Main application entry point
"""
# Don't use eventlet on Windows - use threading instead
import os
import json
from pathlib import Path
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from dotenv import load_dotenv

# Load environment variables FIRST - before importing Config
env_path = Path(__file__).parent.parent / '.env'
print(f"Loading .env from: {env_path}")
print(f".env exists: {env_path.exists()}")
load_dotenv(dotenv_path=str(env_path))

# Now import modules that depend on environment variables
from database import init_db, get_db_session
from models import Meeting, ActionItem, Participant
from agents.audio_listener import AudioListenerAgent
from agents.transcription import TranscriptionAgent
from agents.summarizer import SummarizerAgent
from agents.action_item_extractor import ActionItemExtractorAgent
from agents.calendar_sync import CalendarSyncAgent
from agents.notion_export import NotionExportAgent
from agents.jira_sync import JiraSyncAgent
from agents.translation import TranslationAgent
from agents.task_sync import TaskSyncAgent
from config import Config

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)
app.config['SECRET_KEY'] = Config.SECRET_KEY
CORS(app, resources={r"/*": {"origins": "*"}})
# Use threading mode instead of eventlet for Windows compatibility
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Initialize database
init_db()

# Initialize agents
transcription_agent = TranscriptionAgent()
audio_agent = AudioListenerAgent(socketio, transcription_agent)
summarizer_agent = SummarizerAgent()
action_item_agent = ActionItemExtractorAgent()
task_sync_agent = TaskSyncAgent()
calendar_sync_agent = CalendarSyncAgent()
notion_export_agent = NotionExportAgent()
jira_sync_agent = JiraSyncAgent()
translation_agent = TranslationAgent()

# Print configuration on startup
print("\n" + "="*60)
print("CONFIGURATION CHECK:")
print("="*60)
print(f"Transcription Model: {Config.TRANSCRIPTION_MODEL}")
print(f"Deepgram API Key: {'SET' if Config.DEEPGRAM_API_KEY else 'NOT SET'}")
print(f"Euron API: {'ENABLED' if Config.USE_EURON_API else 'DISABLED'}")
print(f"Euron API Key: {'SET' if Config.EURON_API_KEY else 'NOT SET'}")
print("="*60 + "\n")

# Global state
active_meetings = {}


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "AI Meeting Summarizer"})


@app.route('/api/meetings', methods=['GET'])
def get_meetings():
    """Get all meetings"""
    session = get_db_session()
    meetings = session.query(Meeting).order_by(Meeting.start_time.desc()).all()
    return jsonify([meeting.to_dict() for meeting in meetings])


@app.route('/api/meetings/<int:meeting_id>', methods=['GET'])
def get_meeting(meeting_id):
    """Get specific meeting details"""
    session = get_db_session()
    meeting = session.query(Meeting).filter_by(id=meeting_id).first()
    if not meeting:
        return jsonify({"error": "Meeting not found"}), 404
    return jsonify(meeting.to_dict())


@app.route('/api/meetings/<int:meeting_id>/action-items', methods=['GET'])
def get_action_items(meeting_id):
    """Get action items for a meeting"""
    session = get_db_session()
    action_items = session.query(ActionItem).filter_by(meeting_id=meeting_id).all()
    return jsonify([item.to_dict() for item in action_items])


@app.route('/api/action-items/<int:item_id>/complete', methods=['PUT'])
def complete_action_item(item_id):
    """Mark action item as complete"""
    session = get_db_session()
    action_item = session.query(ActionItem).filter_by(id=item_id).first()
    if not action_item:
        return jsonify({"error": "Action item not found"}), 404
    
    action_item.completed = True
    session.commit()
    return jsonify(action_item.to_dict())


@app.route('/api/meetings/<int:meeting_id>/title', methods=['PUT'])
def update_meeting_title(meeting_id):
    """Update meeting title"""
    session = get_db_session()
    meeting = session.query(Meeting).filter_by(id=meeting_id).first()
    if not meeting:
        return jsonify({"error": "Meeting not found"}), 404
    
    data = request.get_json()
    new_title = data.get('title', '').strip()
    
    if not new_title:
        return jsonify({"error": "Title cannot be empty"}), 400
    
    meeting.title = new_title
    session.commit()
    
    return jsonify({"success": True, "meeting": meeting.to_dict()})


@app.route('/data/audio/<path:filename>')
def serve_audio(filename):
    """Serve audio files"""
    try:
        audio_dir = Config.AUDIO_DIR
        file_path = audio_dir / filename
        
        if not file_path.exists():
            return jsonify({"error": "Audio file not found"}), 404
        
        return send_file(str(file_path), mimetype='audio/wav')
    except Exception as e:
        print(f"Error serving audio file: {e}")
        return jsonify({"error": "Error serving audio file"}), 500


# ============ GOOGLE CALENDAR SYNC ENDPOINTS ============

@app.route('/api/google/available', methods=['GET'])
def google_available():
    """Check if Google Calendar API is available"""
    return jsonify({
        "available": calendar_sync_agent.is_available()
    })


@app.route('/api/google/auth-status', methods=['GET'])
def google_auth_status():
    """Check if user is authenticated with Google"""
    if not calendar_sync_agent.is_available():
        return jsonify({
            "authenticated": False,
            "available": False,
            "message": "Google Calendar API not installed"
        })
    
    return jsonify({
        "authenticated": calendar_sync_agent.is_authenticated(),
        "available": True
    })


@app.route('/api/google/auth-url', methods=['GET'])
def get_google_auth_url():
    """Get Google OAuth URL"""
    try:
        auth_url = calendar_sync_agent.get_auth_url()
        return jsonify({"auth_url": auth_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/google/callback', methods=['GET'])
def google_callback():
    """Handle Google OAuth callback"""
    try:
        code = request.args.get('code')
        if not code:
            return jsonify({"error": "No authorization code provided"}), 400
        
        calendar_sync_agent.complete_auth(code)
        
        # Redirect to frontend with success message
        return '''
        <html>
            <body>
                <h2>Authentication Successful!</h2>
                <p>You can close this window and return to the app.</p>
                <script>window.close();</script>
            </body>
        </html>
        '''
    except Exception as e:
        return f"<h2>Authentication Failed</h2><p>{str(e)}</p>", 500


@app.route('/api/action-items/<int:item_id>/sync-calendar', methods=['POST'])
def sync_action_item_to_calendar(item_id):
    """Sync action item to Google Calendar"""
    session = get_db_session()
    try:
        action_item = session.query(ActionItem).filter_by(id=item_id).first()
        if not action_item:
            return jsonify({"error": "Action item not found"}), 404
        
        if not calendar_sync_agent.is_authenticated():
            return jsonify({"error": "Not authenticated with Google Calendar"}), 401
        
        # Sync to calendar
        event_id = calendar_sync_agent.sync_action_item(action_item)
        
        # Update database
        action_item.synced_to_calendar = True
        action_item.external_id = event_id
        session.commit()
        
        return jsonify({
            "success": True,
            "event_id": event_id,
            "action_item": action_item.to_dict()
        })
    except Exception as e:
        print(f"Error syncing to calendar: {e}")
        session.rollback()
        return jsonify({"error": str(e)}), 500


@app.route('/api/meetings/<int:meeting_id>/sync-all-calendar', methods=['POST'])
def sync_all_to_calendar(meeting_id):
    """Sync all action items from a meeting to Google Calendar"""
    session = get_db_session()
    try:
        meeting = session.query(Meeting).filter_by(id=meeting_id).first()
        if not meeting:
            return jsonify({"error": "Meeting not found"}), 404
        
        if not calendar_sync_agent.is_authenticated():
            return jsonify({"error": "Not authenticated with Google Calendar"}), 401
        
        synced_count = 0
        errors = []
        
        for action_item in meeting.action_items:
            if not action_item.synced_to_calendar:
                try:
                    event_id = calendar_sync_agent.sync_action_item(action_item)
                    action_item.synced_to_calendar = True
                    action_item.external_id = event_id
                    synced_count += 1
                except Exception as e:
                    errors.append(f"Item {action_item.id}: {str(e)}")
        
        session.commit()
        
        return jsonify({
            "success": True,
            "synced_count": synced_count,
            "total_items": len(meeting.action_items),
            "errors": errors
        })
    except Exception as e:
        print(f"Error syncing meeting to calendar: {e}")
        session.rollback()
        return jsonify({"error": str(e)}), 500


# ============ NOTION EXPORT ENDPOINTS ============

@app.route('/api/notion/configure', methods=['POST'])
def configure_notion():
    """Configure Notion API key and database"""
    global notion_export_agent
    
    try:
        data = request.get_json()
        api_key = data.get('api_key')
        database_id = data.get('database_id')
        
        if not api_key:
            return jsonify({"error": "API key is required"}), 400
        
        # Initialize Notion client
        notion_export_agent = NotionExportAgent(api_key)
        
        if database_id:
            notion_export_agent.set_database(database_id)
        
        # Test connection
        try:
            notion_export_agent.test_connection()
            return jsonify({"success": True, "message": "Notion configured successfully"})
        except Exception as e:
            return jsonify({"error": f"Notion connection test failed: {str(e)}"}), 400
    
    except Exception as e:
        print(f"Error configuring Notion: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/notion/status', methods=['GET'])
def notion_status():
    """Check Notion connection status"""
    return jsonify({
        "connected": notion_export_agent.is_authenticated()
    })


@app.route('/api/meetings/<int:meeting_id>/export-notion', methods=['POST'])
def export_to_notion(meeting_id):
    """Export meeting to Notion"""
    session = get_db_session()
    try:
        meeting = session.query(Meeting).filter_by(id=meeting_id).first()
        if not meeting:
            return jsonify({"error": "Meeting not found"}), 404
        
        if not notion_export_agent.is_authenticated():
            return jsonify({"error": "Notion not configured"}), 401
        
        # Export to Notion
        notion_page_id = notion_export_agent.export_meeting(meeting)
        
        return jsonify({
            "success": True,
            "page_id": notion_page_id,
            "message": "Meeting exported to Notion successfully"
        })
    
    except Exception as e:
        print(f"Error exporting to Notion: {e}")
        return jsonify({"error": str(e)}), 500


# ============ JIRA SYNC ENDPOINTS ============

@app.route('/api/jira/configure', methods=['POST'])
def configure_jira():
    """Configure Jira connection"""
    global jira_sync_agent
    
    try:
        data = request.get_json()
        server_url = data.get('server_url')
        email = data.get('email')
        api_token = data.get('api_token')
        project_key = data.get('project_key')
        
        if not all([server_url, email, api_token, project_key]):
            return jsonify({"error": "All fields are required"}), 400
        
        # Configure Jira client
        jira_sync_agent.configure(server_url, email, api_token, project_key)
        
        # Test connection
        try:
            jira_sync_agent.test_connection()
            return jsonify({"success": True, "message": "Jira configured successfully"})
        except Exception as e:
            return jsonify({"error": f"Jira connection test failed: {str(e)}"}), 400
    
    except Exception as e:
        print(f"Error configuring Jira: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/jira/status', methods=['GET'])
def jira_status():
    """Check Jira connection status"""
    return jsonify({
        "connected": jira_sync_agent.is_authenticated()
    })


@app.route('/api/action-items/<int:item_id>/sync-jira', methods=['POST'])
def sync_action_item_to_jira(item_id):
    """Sync action item to Jira"""
    session = get_db_session()
    try:
        action_item = session.query(ActionItem).filter_by(id=item_id).first()
        if not action_item:
            return jsonify({"error": "Action item not found"}), 404
        
        if not jira_sync_agent.is_authenticated():
            return jsonify({"error": "Jira not configured"}), 401
        
        # Sync to Jira
        issue_key = jira_sync_agent.sync_action_item(action_item)
        
        # Update database
        action_item.synced_to_jira = True
        action_item.external_id = issue_key
        session.commit()
        
        return jsonify({
            "success": True,
            "issue_key": issue_key,
            "action_item": action_item.to_dict()
        })
    except Exception as e:
        print(f"Error syncing to Jira: {e}")
        session.rollback()
        return jsonify({"error": str(e)}), 500


@app.route('/api/meetings/<int:meeting_id>/sync-all-jira', methods=['POST'])
def sync_all_to_jira(meeting_id):
    """Sync all action items from a meeting to Jira"""
    session = get_db_session()
    try:
        meeting = session.query(Meeting).filter_by(id=meeting_id).first()
        if not meeting:
            return jsonify({"error": "Meeting not found"}), 404
        
        if not jira_sync_agent.is_authenticated():
            return jsonify({"error": "Jira not configured"}), 401
        
        synced_count = 0
        errors = []
        
        for action_item in meeting.action_items:
            if not action_item.synced_to_jira:
                try:
                    issue_key = jira_sync_agent.sync_action_item(action_item)
                    action_item.synced_to_jira = True
                    action_item.external_id = issue_key
                    synced_count += 1
                except Exception as e:
                    errors.append(f"Item {action_item.id}: {str(e)}")
        
        session.commit()
        
        return jsonify({
            "success": True,
            "synced_count": synced_count,
            "total_items": len(meeting.action_items),
            "errors": errors
        })
    except Exception as e:
        print(f"Error syncing meeting to Jira: {e}")
        session.rollback()
        return jsonify({"error": str(e)}), 500


# ============ TRANSLATION ENDPOINTS ============

@app.route('/api/translation/languages', methods=['GET'])
def get_supported_languages():
    """Get supported translation languages"""
    return jsonify(translation_agent.get_supported_languages())


@app.route('/api/meetings/<int:meeting_id>/translate', methods=['POST'])
def translate_meeting(meeting_id):
    """Translate meeting transcript"""
    session = get_db_session()
    try:
        meeting = session.query(Meeting).filter_by(id=meeting_id).first()
        if not meeting:
            return jsonify({"error": "Meeting not found"}), 404
        
        data = request.get_json()
        target_language = data.get('language', 'es')
        
        # Get transcript text
        import json
        transcript_data = json.loads(meeting.transcript) if meeting.transcript else {}
        transcript_text = transcript_data.get('text', '')
        
        if not transcript_text:
            return jsonify({"error": "No transcript available"}), 400
        
        # Translate
        translated_text = translation_agent.translate_text(transcript_text, target_language)
        
        # Translate summary if available
        translated_summary = None
        if meeting.summary:
            translated_summary = translation_agent.translate_text(meeting.summary, target_language)
        
        return jsonify({
            "success": True,
            "language": target_language,
            "translated_transcript": translated_text,
            "translated_summary": translated_summary
        })
    
    except Exception as e:
        print(f"Error translating meeting: {e}")
        return jsonify({"error": str(e)}), 500


@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print('Client connected')
    emit('connection_status', {'status': 'connected'})


@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print('Client disconnected')


@socketio.event
def start_recording(data):
    """Start recording a meeting"""
    print(f"[DEBUG] Received start_recording event with data: {data}")
    meeting_title = data.get('title', 'Untitled Meeting')
    participants_str = data.get('participants', '')
    
    # Create meeting in database
    session = get_db_session()
    meeting = Meeting(title=meeting_title)
    session.add(meeting)
    session.commit()
    meeting_id = meeting.id
    print(f"[DEBUG] Created meeting {meeting_id} with title: {meeting_title}")
    
    # Add participants if provided
    if participants_str:
        participant_names = [name.strip() for name in participants_str.split(',') if name.strip()]
        for name in participant_names:
            participant = Participant(meeting_id=meeting_id, name=name)
            session.add(participant)
        session.commit()
        print(f"[DEBUG] Added {len(participant_names)} participants to meeting {meeting_id}")
    
    # Store active meeting
    active_meetings[meeting_id] = {
        'meeting': meeting,
        'audio_data': [],
        'transcripts': []
    }
    
    # Start audio capture
    audio_agent.start_recording(meeting_id)
    
    emit('recording_started', {'meeting_id': meeting_id, 'title': meeting_title})


@socketio.event
def stop_recording(data):
    """Stop recording and process meeting"""
    print(f"[DEBUG] Received stop_recording event with data: {data}")
    meeting_id = data.get('meeting_id')
    
    if meeting_id not in active_meetings:
        print(f"[ERROR] Meeting {meeting_id} not found in active_meetings")
        emit('error', {'message': 'Meeting not found'})
        return
    
    print(f"[DEBUG] Stopping recording for meeting {meeting_id}")
    # Stop audio capture
    audio_file = audio_agent.stop_recording(meeting_id)
    
    # Process the meeting
    emit('processing_status', {'status': 'transcribing', 'progress': 10})
    
    # Transcribe audio
    transcript = transcription_agent.transcribe(audio_file, meeting_id)
    active_meetings[meeting_id]['transcripts'].append(transcript)
    
    emit('processing_status', {'status': 'summarizing', 'progress': 40})
    
    # Generate summary
    summary = summarizer_agent.summarize(transcript)
    
    emit('processing_status', {'status': 'extracting_actions', 'progress': 70})
    
    # Extract action items
    action_items = action_item_agent.extract(transcript, summary)
    
    # Save to database
    session = get_db_session()
    meeting = session.query(Meeting).filter_by(id=meeting_id).first()
    # Convert transcript dict to JSON string for SQLite storage
    meeting.transcript = json.dumps(transcript) if isinstance(transcript, dict) else transcript
    meeting.summary = summary
    meeting.end_meeting()
    
    for item_data in action_items:
        action_item = ActionItem(
            meeting_id=meeting_id,
            description=item_data['description'],
            assignee=item_data.get('assignee'),
            due_date=item_data.get('due_date'),
            priority=item_data.get('priority', 'medium')
        )
        session.add(action_item)
    
    session.commit()
    
    emit('processing_status', {'status': 'complete', 'progress': 100})
    emit('meeting_processed', {
        'meeting_id': meeting_id,
        'summary': summary,
        'action_items': action_items
    })
    
    # Clean up
    del active_meetings[meeting_id]


# Handle audio chunks for live transcription
@socketio.on('audio_chunk_ready')
def handle_audio_chunk(data):
    """Process audio chunk for live transcription"""
    meeting_id = data.get('meeting_id')
    chunk_file = data.get('chunk_file')
    
    print(f"[LIVE] *** HANDLER CALLED *** Processing chunk for meeting {meeting_id}: {chunk_file}")
    
    try:
        # Transcribe the chunk
        print(f"[LIVE] Starting transcription...")
        transcript_result = transcription_agent.transcribe(chunk_file)
        
        if transcript_result and transcript_result.get('text'):
            chunk_text = transcript_result['text'].strip()
            
            if chunk_text:
                print(f"[LIVE] Chunk transcribed: {chunk_text[:100]}...")
                
                # Emit to frontend
                socketio.emit('live_transcript_update', {
                    'meeting_id': meeting_id,
                    'text': chunk_text
                }, broadcast=True)
                print(f"[LIVE] Emitted to frontend")
            else:
                print(f"[LIVE] Chunk was empty")
        else:
            print(f"[LIVE] No transcript result")
        
        # Clean up chunk file
        import os
        if os.path.exists(chunk_file):
            os.remove(chunk_file)
            print(f"[LIVE] Cleaned up chunk file")
            
    except Exception as e:
        print(f"[LIVE] Error processing chunk: {e}")
        import traceback
        traceback.print_exc()


@socketio.on('sync_action_items')
def handle_sync_action_items(data):
    """Sync action items to external services"""
    meeting_id = data.get('meeting_id')
    services = data.get('services', [])  # ['google_calendar', 'notion', 'jira']
    
    session = get_db_session()
    meeting = session.query(Meeting).filter_by(id=meeting_id).first()
    action_items = session.query(ActionItem).filter_by(meeting_id=meeting_id).all()
    
    results = task_sync_agent.sync_tasks(meeting, action_items, services)
    
    emit('sync_complete', {'results': results})


if __name__ == '__main__':
    port = int(os.getenv('FLASK_PORT', 5000))
    host = os.getenv('FLASK_HOST', 'localhost')
    
    # Use 127.0.0.1 instead of 'localhost' to avoid eventlet DNS issues on Windows
    if host == 'localhost':
        host = '127.0.0.1'
    
    print(f"\n{'='*60}")
    print(f"AI Meeting Summarizer Backend Starting...")
    print(f"{'='*60}")
    print(f"Host: {host}")
    print(f"Port: {port}")
    print(f"{'='*60}\n")
    socketio.run(app, host=host, port=port, debug=False, allow_unsafe_werkzeug=True, use_reloader=False)

