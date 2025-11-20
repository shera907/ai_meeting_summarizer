#!/usr/bin/env python3
"""
Quick setup for Euron.one API
"""
import os
from pathlib import Path

def setup_euron():
    """Setup Euron.one API configuration"""
    print("=" * 60)
    print("🚀 Euron.one API Setup for Meeting Summarizer")
    print("=" * 60)
    print()
    
    # Get API key
    print("📋 From your Euron.one dashboard, you have:")
    print("   API Key: euri-dg8...bbo")
    print()
    
    api_key = input("📝 Paste your COMPLETE Euron.one API key here: ").strip()
    
    if not api_key.startswith('euri-'):
        print("⚠️  Warning: Euron.one API keys typically start with 'euri-'")
        confirm = input("   Continue anyway? (y/n): ")
        if confirm.lower() != 'y':
            return
    
    # Get model preference
    print()
    print("🤖 Choose your model:")
    print("   1. gpt-4.1-mini (Recommended - best balance)")
    print("   2. gpt-4.1-nano (Fastest & cheapest)")
    print("   3. gpt-4.0-ultra (Best quality)")
    
    model_choice = input("   Enter choice (1-3) [default: 1]: ").strip() or "1"
    
    models = {
        "1": "gpt-4.1-mini",
        "2": "gpt-4.1-nano",
        "3": "gpt-4.0-ultra"
    }
    model = models.get(model_choice, "gpt-4.1-mini")
    
    # Create .env content
    env_content = f"""# ============================================
# AI Meeting Summarizer - Euron.one Configuration
# ============================================

# === EURON.ONE API ===
USE_EURON_API=true
EURON_API_KEY={api_key}
EURON_API_BASE=https://api.euron.one/api/v1/euri
EURON_MODEL={model}

# === Transcription (Local Whisper - FREE) ===
TRANSCRIPTION_MODEL=whisper

# === Local Model ===
USE_LOCAL_MODEL=false
LOCAL_MODEL_PATH=./models/llama-2-7b-chat.gguf

# === Other APIs (not needed with Euron) ===
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
DEEPGRAM_API_KEY=
ASSEMBLYAI_API_KEY=

# === Backend ===
FLASK_PORT=5000
FLASK_HOST=localhost
DEBUG=true
SECRET_KEY=euron-meeting-summarizer-secret-key

# === Database ===
DATABASE_PATH=./data/meetings.db

# === Integrations (Optional) ===
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
NOTION_API_KEY=
JIRA_API_URL=
JIRA_API_TOKEN=
JIRA_EMAIL=

# === Settings ===
SAMPLE_RATE=16000
CHANNELS=1
AUTO_CLEANUP_DAYS=30
ENABLE_NOTIFICATIONS=true
"""
    
    # Write .env file
    env_path = Path('.env')
    
    if env_path.exists():
        backup = input("\n⚠️  .env file exists. Create backup? (Y/n): ").strip().lower() or 'y'
        if backup == 'y':
            import shutil
            shutil.copy('.env', '.env.backup')
            print("✓ Backup created: .env.backup")
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print()
    print("=" * 60)
    print("✅ Configuration Complete!")
    print("=" * 60)
    print()
    print("📁 Created: .env")
    print(f"🤖 Model: {model}")
    print("🎙️  Transcription: Whisper (local, free)")
    print()
    print("🚀 Next steps:")
    print("   1. Run: npm start")
    print("   2. Record a test meeting")
    print("   3. Enjoy AI summaries!")
    print()
    print("💰 Cost: ~$0.01 per meeting (very cheap!)")
    print()

if __name__ == '__main__':
    try:
        setup_euron()
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled")
    except Exception as e:
        print(f"\n❌ Error: {e}")

