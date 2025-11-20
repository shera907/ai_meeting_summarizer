#!/usr/bin/env python3
"""
Quick install script for minimal setup (Euron.one + Whisper)
"""
import subprocess
import sys

def install_minimal():
    """Install only the essential packages"""
    print("=" * 60)
    print("🚀 Installing Minimal Requirements")
    print("   (Euron.one API + Whisper Transcription)")
    print("=" * 60)
    print()
    
    packages = [
        "flask==3.0.0",
        "flask-cors==4.0.0",
        "flask-socketio==5.3.5",
        "sounddevice==0.4.6",
        "soundfile==0.12.1",
        "openai-whisper==20231117",
        "openai==1.12.0",
        "sqlalchemy==2.0.25",
        "python-dotenv==1.0.1",
        "requests==2.31.0",
        "python-dateutil==2.8.2",
        "numpy",
        "ffmpeg-python"
    ]
    
    print("📦 Installing packages...")
    print()
    
    for package in packages:
        print(f"   Installing {package}...")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", package
            ], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            print(f"   ✓ {package}")
        except subprocess.CalledProcessError as e:
            print(f"   ⚠️  Warning: {package} - {e}")
    
    print()
    print("=" * 60)
    print("✅ Installation Complete!")
    print("=" * 60)
    print()
    print("📦 Installed:")
    print("   • Flask backend")
    print("   • OpenAI client (for Euron.one)")
    print("   • Whisper (local transcription)")
    print("   • Audio recording libraries")
    print("   • SQLite database")
    print()
    print("🚀 Next steps:")
    print("   1. Run: python setup_euron.py")
    print("   2. Run: npm start")
    print()
    print("💡 Skipped optional packages:")
    print("   • Anthropic (Claude) - not needed for Euron.one")
    print("   • LangChain/CrewAI - not needed for basic usage")
    print("   • Local LLMs - not needed with Euron.one")
    print("   • PyAudio - using SoundDevice instead")
    print()

if __name__ == '__main__':
    try:
        install_minimal()
    except KeyboardInterrupt:
        print("\n\n❌ Installation cancelled")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTry manually:")
        print("   pip install -r requirements-minimal.txt")

