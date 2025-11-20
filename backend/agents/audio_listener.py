"""
Audio Listener Agent
Captures audio from the system microphone
"""
import sounddevice as sd
import soundfile as sf
import numpy as np
import threading
import time
from datetime import datetime
from pathlib import Path
from config import Config


class AudioListenerAgent:
    """Agent responsible for capturing audio during meetings"""
    
    def __init__(self, socketio, transcription_agent=None):
        self.socketio = socketio
        self.transcription_agent = transcription_agent
        self.active_recordings = {}
        self.sample_rate = Config.SAMPLE_RATE
        self.channels = Config.CHANNELS
        self.chunk_duration = 10  # seconds for live transcription
    
    def start_recording(self, meeting_id):
        """Start recording audio for a meeting"""
        print(f"Starting audio recording for meeting {meeting_id}")
        
        # Initialize recording buffer
        self.active_recordings[meeting_id] = {
            'audio_data': [],
            'stream': None,
            'recording': True,
            'chunk_buffer': [],
            'last_chunk_time': time.time()
        }
        
        # Callback for audio stream
        def audio_callback(indata, frames, time_info, status):
            if status:
                print(f"Audio callback status: {status}")
            if meeting_id in self.active_recordings and self.active_recordings[meeting_id]['recording']:
                self.active_recordings[meeting_id]['audio_data'].append(indata.copy())
                self.active_recordings[meeting_id]['chunk_buffer'].append(indata.copy())
        
        # Start audio stream
        stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            callback=audio_callback,
            dtype=np.float32
        )
        stream.start()
        self.active_recordings[meeting_id]['stream'] = stream
        
        # Start chunked transcription thread
        chunk_thread = threading.Thread(
            target=self._process_chunks,
            args=(meeting_id,),
            daemon=True
        )
        chunk_thread.start()
        
        # Emit status
        self.socketio.emit('audio_status', {
            'meeting_id': meeting_id,
            'status': 'recording'
        })
    
    def _process_chunks(self, meeting_id):
        """Process audio chunks for live transcription"""
        print(f"[LIVE] Starting chunk processor for meeting {meeting_id}")
        
        while meeting_id in self.active_recordings and self.active_recordings[meeting_id]['recording']:
            time.sleep(self.chunk_duration)
            
            if meeting_id not in self.active_recordings:
                break
            
            recording_data = self.active_recordings[meeting_id]
            
            # Check if we have buffered audio
            if recording_data['chunk_buffer']:
                try:
                    # Get chunk data
                    chunk_data = np.concatenate(recording_data['chunk_buffer'], axis=0)
                    recording_data['chunk_buffer'] = []  # Clear buffer
                    
                    # Save chunk to temp file
                    temp_filename = f"chunk_{meeting_id}_{int(time.time())}.wav"
                    temp_filepath = Config.AUDIO_DIR / temp_filename
                    
                    sf.write(str(temp_filepath), chunk_data, self.sample_rate)
                    
                    print(f"[LIVE] Saved chunk: {temp_filename} ({len(chunk_data)} samples)")
                    
                    # Transcribe directly if transcription agent is available
                    if self.transcription_agent:
                        try:
                            print(f"[LIVE] Transcribing chunk...")
                            transcript_result = self.transcription_agent.transcribe(str(temp_filepath))
                            
                            if transcript_result and transcript_result.get('text'):
                                chunk_text = transcript_result['text'].strip()
                                
                                if chunk_text:
                                    print(f"[LIVE] Chunk transcribed: {chunk_text[:100]}...")
                                    
                                    # Emit to frontend via socketio
                                    self.socketio.emit('live_transcript_update', {
                                        'meeting_id': meeting_id,
                                        'text': chunk_text
                                    })
                                    print(f"[LIVE] Emitted to frontend")
                                else:
                                    print(f"[LIVE] Chunk was empty")
                            else:
                                print(f"[LIVE] No transcript result")
                            
                            # Clean up chunk file
                            import os
                            if os.path.exists(str(temp_filepath)):
                                os.remove(str(temp_filepath))
                                
                        except Exception as e:
                            print(f"[LIVE] Error transcribing chunk: {e}")
                            import traceback
                            traceback.print_exc()
                    else:
                        # Fallback: emit event (but this doesn't work from threads)
                        self.socketio.emit('audio_chunk_ready', {
                            'meeting_id': meeting_id,
                            'chunk_file': str(temp_filepath)
                        })
                    
                except Exception as e:
                    print(f"[LIVE] Error processing chunk: {e}")
        
        print(f"[LIVE] Chunk processor stopped for meeting {meeting_id}")
    
    def stop_recording(self, meeting_id):
        """Stop recording and save audio file"""
        if meeting_id not in self.active_recordings:
            return None
        
        print(f"Stopping audio recording for meeting {meeting_id}")
        
        recording_data = self.active_recordings[meeting_id]
        recording_data['recording'] = False
        
        # Stop stream
        if recording_data['stream']:
            recording_data['stream'].stop()
            recording_data['stream'].close()
        
        # Concatenate audio data
        if recording_data['audio_data']:
            audio_array = np.concatenate(recording_data['audio_data'], axis=0)
            
            # Save to file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"meeting_{meeting_id}_{timestamp}.wav"
            filepath = Config.AUDIO_DIR / filename
            
            sf.write(str(filepath), audio_array, self.sample_rate)
            print(f"Audio saved to {filepath}")
            
            # Clean up
            del self.active_recordings[meeting_id]
            
            # Emit status
            self.socketio.emit('audio_status', {
                'meeting_id': meeting_id,
                'status': 'saved',
                'file': str(filepath)
            })
            
            return str(filepath)
        
        return None
    
    def get_recording_status(self, meeting_id):
        """Get status of a recording"""
        if meeting_id in self.active_recordings:
            return 'recording'
        return 'stopped'

