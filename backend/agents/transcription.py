"""
Transcription Agent
Transcribes audio using Whisper, Deepgram, or AssemblyAI
"""
import os
from pathlib import Path
from config import Config

# Try to import whisper, but make it optional
try:
    import whisper
    WHISPER_AVAILABLE = True
except Exception as e:
    print(f"WARNING: Whisper not available: {e}")
    print("   Transcription will use API or fallback")
    WHISPER_AVAILABLE = False
    whisper = None


class TranscriptionAgent:
    """Agent responsible for transcribing audio to text"""
    
    def __init__(self):
        self.model_type = Config.TRANSCRIPTION_MODEL
        self.whisper_model = None
        
        if self.model_type == 'whisper' and WHISPER_AVAILABLE:
            try:
                print("Loading Whisper model...")
                self.whisper_model = whisper.load_model("base")
                print("OK: Whisper model loaded")
            except Exception as e:
                print(f"WARNING: Whisper loading failed: {e}")
                print("   Will use fallback transcription")
                self.whisper_model = None
        elif self.model_type == 'whisper' and not WHISPER_AVAILABLE:
            print("WARNING: Whisper requested but not available")
            print("   Using fallback transcription")
    
    def transcribe(self, audio_file, meeting_id=None):
        """Transcribe audio file to text"""
        if not audio_file or not os.path.exists(audio_file):
            raise ValueError(f"Audio file not found: {audio_file}")
        
        print(f"Transcribing audio file: {audio_file}")
        
        if self.model_type == 'whisper':
            return self._transcribe_whisper(audio_file)
        elif self.model_type == 'deepgram':
            return self._transcribe_deepgram(audio_file)
        elif self.model_type == 'assemblyai':
            return self._transcribe_assemblyai(audio_file)
        else:
            raise ValueError(f"Unknown transcription model: {self.model_type}")
    
    def _transcribe_whisper(self, audio_file):
        """Transcribe using Whisper"""
        if not self.whisper_model:
            print("WARNING: Whisper model not loaded, using fallback")
            return self._transcribe_fallback(audio_file)
        
        try:
            result = self.whisper_model.transcribe(audio_file)
            transcript = result['text']
            
            # Get segments with timestamps
            segments = []
            for segment in result.get('segments', []):
                segments.append({
                    'start': segment['start'],
                    'end': segment['end'],
                    'text': segment['text']
                })
            
            return {
                'text': transcript,
                'segments': segments,
                'language': result.get('language', 'en')
            }
        except Exception as e:
            print(f"Whisper transcription error: {e}")
            return self._transcribe_fallback(audio_file)
    
    def _transcribe_fallback(self, audio_file):
        """Fallback when Whisper is not available"""
        return {
            'text': f"[Audio recorded from {audio_file}]\n\nTranscription temporarily unavailable. Please:\n1. Install Visual C++ Redistributables\n2. Or use Deepgram/AssemblyAI API\n3. Or wait for transcription service setup",
            'segments': [],
            'language': 'en'
        }
    
    def _transcribe_deepgram(self, audio_file):
        """Transcribe using Deepgram API"""
        try:
            import httpx
            
            if not Config.DEEPGRAM_API_KEY:
                raise ValueError("DEEPGRAM_API_KEY not configured")
            
            print(f"Transcribing with Deepgram: {audio_file}")
            
            # Read audio file
            with open(audio_file, 'rb') as f:
                audio_data = f.read()
            
            file_size = len(audio_data)
            print(f"Audio file size: {file_size / 1024:.2f} KB")
            
            # Make direct API call to Deepgram with longer timeout
            url = "https://api.deepgram.com/v1/listen?model=nova-2&smart_format=true"
            headers = {
                "Authorization": f"Token {Config.DEEPGRAM_API_KEY}",
                "Content-Type": "audio/wav"
            }
            
            print("Sending request to Deepgram...")
            response = httpx.post(url, headers=headers, content=audio_data, timeout=60.0)
            response.raise_for_status()
            
            result = response.json()
            transcript = result["results"]["channels"][0]["alternatives"][0]["transcript"]
            
            if not transcript or transcript.strip() == "":
                print("Deepgram returned empty transcript (no speech detected)")
                transcript = ""
            
            print(f"Deepgram transcription successful: {len(transcript)} characters")
            
            return {
                'text': transcript,
                'segments': [],
                'language': 'en'
            }
        except httpx.TimeoutException as e:
            print(f"Deepgram timeout error: {e}")
            print("Audio file may be too long or network is slow. Using fallback.")
            return self._transcribe_fallback(audio_file)
        except httpx.HTTPStatusError as e:
            print(f"Deepgram HTTP error: {e}")
            print(f"Status code: {e.response.status_code}")
            print(f"Response: {e.response.text[:200]}")
            return self._transcribe_fallback(audio_file)
        except Exception as e:
            print(f"Deepgram transcription error: {e}")
            import traceback
            traceback.print_exc()
            # Fallback
            return self._transcribe_fallback(audio_file)
    
    def _transcribe_assemblyai(self, audio_file):
        """Transcribe using AssemblyAI API"""
        try:
            import assemblyai as aai
            
            if not Config.ASSEMBLYAI_API_KEY:
                raise ValueError("ASSEMBLYAI_API_KEY not configured")
            
            aai.settings.api_key = Config.ASSEMBLYAI_API_KEY
            transcriber = aai.Transcriber()
            
            transcript = transcriber.transcribe(audio_file)
            
            return {
                'text': transcript.text,
                'segments': [],
                'language': 'en'
            }
        except Exception as e:
            print(f"AssemblyAI transcription error: {e}")
            # Fallback to Whisper
            return self._transcribe_whisper(audio_file)

