#!/usr/bin/env python3
"""
Quick test script to verify installation
"""
import sys

def test_imports():
    """Test if all required packages are installed"""
    print("Testing Python dependencies...\n")
    
    tests = [
        ("Flask", "flask"),
        ("Flask-CORS", "flask_cors"),
        ("Flask-SocketIO", "flask_socketio"),
        ("SQLAlchemy", "sqlalchemy"),
        ("Whisper", "whisper"),
        ("OpenAI", "openai"),
        ("SoundDevice", "sounddevice"),
        ("SoundFile", "soundfile"),
        ("NumPy", "numpy"),
        ("Python-dotenv", "dotenv"),
    ]
    
    passed = 0
    failed = 0
    
    for name, module in tests:
        try:
            __import__(module)
            print(f"✓ {name}")
            passed += 1
        except ImportError as e:
            print(f"✗ {name} - {e}")
            failed += 1
    
    print(f"\n{passed} passed, {failed} failed")
    
    if failed > 0:
        print("\nTo install missing packages, run:")
        print("pip install -r requirements.txt")
        return False
    
    return True

def test_config():
    """Test if configuration is set up"""
    print("\n\nTesting configuration...\n")
    
    try:
        import os
        from pathlib import Path
        
        # Check if .env exists
        if Path('.env').exists():
            print("✓ .env file found")
        else:
            print("⚠ .env file not found - copy .env.example to .env")
        
        # Check data directories
        data_dir = Path('data')
        audio_dir = Path('data/audio')
        
        if data_dir.exists():
            print("✓ data/ directory exists")
        else:
            print("⚠ data/ directory will be created on first run")
        
        if audio_dir.exists():
            print("✓ data/audio/ directory exists")
        else:
            print("⚠ data/audio/ directory will be created on first run")
        
        return True
    
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False

def test_database():
    """Test database connection"""
    print("\n\nTesting database...\n")
    
    try:
        from backend.database import init_db
        init_db()
        print("✓ Database initialized successfully")
        return True
    except Exception as e:
        print(f"✗ Database test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("AI Meeting Summarizer - Installation Test")
    print("=" * 50)
    
    # Test imports
    if not test_imports():
        print("\n❌ Import tests failed. Please install missing dependencies.")
        sys.exit(1)
    
    # Test config
    test_config()
    
    # Test database
    test_database()
    
    print("\n" + "=" * 50)
    print("✅ All tests passed! You're ready to run the app.")
    print("=" * 50)
    print("\nRun: npm start")

if __name__ == '__main__':
    main()

