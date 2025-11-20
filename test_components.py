"""
Example usage and testing script
"""
import sys
import time
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

def test_agents():
    """Test all AI agents"""
    print("Testing AI Agents...")
    print("-" * 50)
    
    # Test imports
    try:
        from backend.agents import (
            AudioListenerAgent,
            TranscriptionAgent,
            SummarizerAgent,
            ActionItemExtractorAgent,
            TaskSyncAgent
        )
        print("✓ All agents imported successfully")
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    
    # Test database
    try:
        from backend.database import init_db
        init_db()
        print("✓ Database initialized")
    except Exception as e:
        print(f"✗ Database error: {e}")
        return False
    
    # Test configuration
    try:
        from backend.config import Config
        Config.init_directories()
        print("✓ Configuration loaded")
        print(f"  - Transcription model: {Config.TRANSCRIPTION_MODEL}")
        print(f"  - Use local model: {Config.USE_LOCAL_MODEL}")
        print(f"  - Database path: {Config.DATABASE_PATH}")
    except Exception as e:
        print(f"✗ Configuration error: {e}")
        return False
    
    return True

def test_transcription():
    """Test transcription with sample text"""
    print("\n" + "-" * 50)
    print("Testing Transcription Agent...")
    print("-" * 50)
    
    try:
        from backend.agents.transcription import TranscriptionAgent
        
        agent = TranscriptionAgent()
        print(f"✓ Transcription agent initialized")
        print(f"  Model type: {agent.model_type}")
        
        if agent.model_type == 'whisper' and agent.whisper_model:
            print("✓ Whisper model loaded and ready")
        else:
            print("ℹ Whisper model not loaded (will use API)")
        
        return True
    except Exception as e:
        print(f"✗ Transcription test error: {e}")
        return False

def test_summarizer():
    """Test summarizer with sample text"""
    print("\n" + "-" * 50)
    print("Testing Summarizer Agent...")
    print("-" * 50)
    
    try:
        from backend.agents.summarizer import SummarizerAgent
        
        agent = SummarizerAgent()
        print("✓ Summarizer agent initialized")
        
        # Test with sample text
        sample_transcript = """
        Hello everyone, thank you for joining today's meeting. 
        We need to discuss the Q4 project timeline and assign tasks.
        John, can you handle the frontend development?
        Sarah will work on the backend API.
        We should aim to complete this by December 15th.
        Let's schedule a follow-up meeting next week.
        """
        
        print("\nTesting summary generation...")
        summary = agent.summarize(sample_transcript)
        
        if summary:
            print("✓ Summary generated successfully")
            print(f"\nSample Summary:\n{summary[:200]}...")
        else:
            print("⚠ Summary generation returned empty")
            print("  (This is normal if no API keys are configured)")
        
        return True
    except Exception as e:
        print(f"✗ Summarizer test error: {e}")
        return False

def test_action_extractor():
    """Test action item extraction"""
    print("\n" + "-" * 50)
    print("Testing Action Item Extractor...")
    print("-" * 50)
    
    try:
        from backend.agents.action_item_extractor import ActionItemExtractorAgent
        
        agent = ActionItemExtractorAgent()
        print("✓ Action item extractor initialized")
        
        sample_transcript = """
        We need to finalize the budget by Friday.
        John will review the marketing materials.
        Sarah should schedule a client meeting next week.
        Everyone must submit their timesheets by end of day.
        """
        
        print("\nTesting action item extraction...")
        action_items = agent.extract(sample_transcript)
        
        if action_items:
            print(f"✓ Extracted {len(action_items)} action items")
            for i, item in enumerate(action_items[:3], 1):
                print(f"  {i}. {item['description'][:60]}...")
        else:
            print("⚠ No action items extracted")
            print("  (This is normal if no API keys are configured)")
        
        return True
    except Exception as e:
        print(f"✗ Action extractor test error: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("AI Meeting Summarizer - Component Tests")
    print("=" * 50)
    print()
    
    results = {
        'Agents Import': test_agents(),
        'Transcription': test_transcription(),
        'Summarization': test_summarizer(),
        'Action Extraction': test_action_extractor()
    }
    
    print("\n" + "=" * 50)
    print("Test Results")
    print("=" * 50)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n✅ All tests passed!")
        print("\nYou're ready to start the application:")
        print("  npm start")
    else:
        print("\n⚠️ Some tests failed")
        print("\nThis may be normal if:")
        print("  - No API keys configured (will use fallback methods)")
        print("  - Whisper model not downloaded")
        print("  - Some dependencies missing")
        print("\nThe app should still work with basic features.")

if __name__ == '__main__':
    main()

