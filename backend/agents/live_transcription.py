"""
Live Transcription Agent
Provides real-time transcription during recording using Deepgram streaming
"""

import asyncio
import json
import threading
from config import Config

try:
    from deepgram import (
        DeepgramClient,
        DeepgramClientOptions,
        LiveTranscriptionEvents,
        LiveOptions,
    )
    DEEPGRAM_STREAMING_AVAILABLE = True
except ImportError:
    DEEPGRAM_STREAMING_AVAILABLE = False
    print("WARNING: Deepgram streaming not available for live transcription")


class LiveTranscriptionAgent:
    """Handles live transcription during recording"""
    
    def __init__(self, socketio):
        self.socketio = socketio
        self.active_sessions = {}
        self.deepgram_client = None
        
        if DEEPGRAM_STREAMING_AVAILABLE and Config.DEEPGRAM_API_KEY:
            try:
                config = DeepgramClientOptions(
                    options={"keepalive": "true"}
                )
                self.deepgram_client = DeepgramClient(Config.DEEPGRAM_API_KEY, config)
                print("Live transcription agent initialized with Deepgram streaming")
            except Exception as e:
                print(f"Error initializing Deepgram streaming: {e}")
    
    def is_available(self):
        """Check if live transcription is available"""
        return DEEPGRAM_STREAMING_AVAILABLE and self.deepgram_client is not None
    
    async def start_live_transcription(self, meeting_id, audio_stream):
        """Start live transcription for a meeting"""
        if not self.is_available():
            print("Live transcription not available")
            return
        
        try:
            # Set up Deepgram streaming connection
            dg_connection = self.deepgram_client.listen.asynclive.v("1")
            
            # Event handlers
            async def on_message(self, result, **kwargs):
                sentence = result.channel.alternatives[0].transcript
                if len(sentence) > 0:
                    # Emit partial transcript to frontend
                    self.socketio.emit('live_transcript', {
                        'meeting_id': meeting_id,
                        'text': sentence,
                        'is_final': result.is_final
                    })
            
            async def on_error(self, error, **kwargs):
                print(f"Live transcription error: {error}")
            
            # Register event handlers
            dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
            dg_connection.on(LiveTranscriptionEvents.Error, on_error)
            
            # Configure streaming options
            options = LiveOptions(
                model="nova-2",
                language="en",
                smart_format=True,
                punctuate=True,
                interim_results=True
            )
            
            # Start connection
            await dg_connection.start(options)
            
            # Store session
            self.active_sessions[meeting_id] = dg_connection
            
            print(f"Live transcription started for meeting {meeting_id}")
            
        except Exception as e:
            print(f"Error starting live transcription: {e}")
    
    async def send_audio_chunk(self, meeting_id, audio_data):
        """Send audio chunk for live transcription"""
        if meeting_id in self.active_sessions:
            try:
                await self.active_sessions[meeting_id].send(audio_data)
            except Exception as e:
                print(f"Error sending audio chunk: {e}")
    
    async def stop_live_transcription(self, meeting_id):
        """Stop live transcription for a meeting"""
        if meeting_id in self.active_sessions:
            try:
                await self.active_sessions[meeting_id].finish()
                del self.active_sessions[meeting_id]
                print(f"Live transcription stopped for meeting {meeting_id}")
            except Exception as e:
                print(f"Error stopping live transcription: {e}")

