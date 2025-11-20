"""
Translation Agent
Translates transcripts to different languages
"""

# Translation API - optional import
try:
    from deep_translator import GoogleTranslator
    TRANSLATION_AVAILABLE = True
except ImportError:
    TRANSLATION_AVAILABLE = False
    print("WARNING: Translation not available. Install deep-translator to enable.")


class TranslationAgent:
    """Translates meeting transcripts"""
    
    def __init__(self):
        self.available = TRANSLATION_AVAILABLE
    
    def is_available(self):
        """Check if translation is available"""
        return self.available
    
    def translate_text(self, text, target_language='es'):
        """
        Translate text to target language
        
        Args:
            text: Text to translate
            target_language: Target language code (e.g., 'es', 'fr', 'de', 'ja', 'zh-CN')
        
        Returns:
            Translated text
        """
        if not self.available:
            raise Exception("Translation not available. Install deep-translator package.")
        
        try:
            translator = GoogleTranslator(source='auto', target=target_language)
            
            # Split into chunks if text is too long
            max_length = 5000
            if len(text) <= max_length:
                return translator.translate(text)
            
            # Translate in chunks
            chunks = [text[i:i+max_length] for i in range(0, len(text), max_length)]
            translated_chunks = [translator.translate(chunk) for chunk in chunks]
            return ' '.join(translated_chunks)
        
        except Exception as e:
            print(f"Translation error: {e}")
            raise
    
    def get_supported_languages(self):
        """Get list of supported languages"""
        return {
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German',
            'it': 'Italian',
            'pt': 'Portuguese',
            'ru': 'Russian',
            'ja': 'Japanese',
            'ko': 'Korean',
            'zh-CN': 'Chinese (Simplified)',
            'zh-TW': 'Chinese (Traditional)',
            'ar': 'Arabic',
            'hi': 'Hindi'
        }

