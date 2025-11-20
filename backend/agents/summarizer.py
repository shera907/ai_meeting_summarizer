"""
Summarizer Agent
Generates meeting summaries using LLMs
"""
from config import Config
from openai import OpenAI

# Optional: Only needed if using Claude API
try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    Anthropic = None


class SummarizerAgent:
    """Agent responsible for summarizing meeting transcripts"""
    
    def __init__(self):
        self.use_local = Config.USE_LOCAL_MODEL
        self.use_euron = Config.USE_EURON_API
        
        if self.use_local:
            self._init_local_model()
        else:
            # Initialize OpenAI client (can be used for official OpenAI or Euron.one)
            if Config.USE_EURON_API and Config.EURON_API_KEY:
                # Use Euron.one API with OpenAI-compatible client
                self.openai_client = OpenAI(
                    api_key=Config.EURON_API_KEY,
                    base_url=Config.EURON_API_BASE
                )
                self.model_name = Config.EURON_MODEL
                print(f"OK: Using Euron.one API with model: {self.model_name}")
            elif Config.OPENAI_API_KEY:
                # Use official OpenAI API
                self.openai_client = OpenAI(api_key=Config.OPENAI_API_KEY)
                self.model_name = "gpt-4-turbo-preview"
                print("OK: Using official OpenAI API")
            else:
                self.openai_client = None
                self.model_name = None
            
            # Optional: Anthropic/Claude support (only if installed)
            if ANTHROPIC_AVAILABLE and Config.ANTHROPIC_API_KEY:
                self.anthropic_client = Anthropic(api_key=Config.ANTHROPIC_API_KEY)
            else:
                self.anthropic_client = None
    
    def _init_local_model(self):
        """Initialize local LLM model"""
        try:
            from llama_cpp import Llama
            self.local_model = Llama(
                model_path=Config.LOCAL_MODEL_PATH,
                n_ctx=4096,
                n_threads=4
            )
        except Exception as e:
            print(f"Error loading local model: {e}")
            self.use_local = False
    
    def summarize(self, transcript_data):
        """Generate a comprehensive meeting summary"""
        transcript_text = transcript_data.get('text', '') if isinstance(transcript_data, dict) else transcript_data
        
        prompt = self._create_summary_prompt(transcript_text)
        
        if self.use_local:
            return self._summarize_local(prompt)
        elif self.openai_client:
            return self._summarize_openai(prompt)
        elif self.anthropic_client:
            return self._summarize_anthropic(prompt)
        else:
            return self._fallback_summary(transcript_text)
    
    def _create_summary_prompt(self, transcript):
        """Create prompt for summarization"""
        return f"""You are an expert meeting analyst and summarizer. Analyze the following meeting transcript and provide a COMPREHENSIVE, DETAILED summary.

Your summary should be thorough and include:

1. **Meeting Overview**
   - Purpose and context of the meeting
   - Overall tone and atmosphere
   - Duration and flow

2. **Main Topics Discussed**
   - List ALL major topics/themes covered
   - For each topic, provide 2-3 sentences of detail
   - Include any background context mentioned

3. **Key Points and Insights**
   - Important facts, data, or metrics mentioned
   - Critical insights or observations shared
   - Any concerns or challenges raised
   - Opportunities or ideas discussed

4. **Decisions Made**
   - All concrete decisions or agreements
   - Who made or approved each decision
   - Reasoning behind each decision

5. **Action Items and Next Steps**
   - Detailed list of tasks assigned
   - Who is responsible for each task
   - Deadlines mentioned
   - Dependencies between tasks

6. **Discussion Details**
   - Key questions asked and answers provided
   - Different viewpoints or opinions expressed
   - Any debates or discussions that occurred
   - Consensus reached on various points

7. **Participants and Contributions**
   - Who spoke and their roles (if identifiable)
   - Main contributions from each participant
   - Level of engagement

8. **Follow-up Items**
   - Future meetings planned
   - Information or resources needed
   - Open questions requiring answers

Meeting Transcript:
{transcript}

Please provide a well-structured, DETAILED summary with specific examples and quotes where relevant. Make it comprehensive enough that someone who missed the meeting can fully understand what happened:"""
    
    def _summarize_openai(self, prompt):
        """Summarize using OpenAI API (official or Euron.one)"""
        try:
            response = self.openai_client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are an expert meeting analyst who provides comprehensive, detailed summaries. Always be thorough and include specific details, quotes, and context."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=2500  # Increased for more detailed summaries
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"AI summarization error: {e}")
            return None
    
    def _summarize_anthropic(self, prompt):
        """Summarize using Claude"""
        try:
            response = self.anthropic_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1500,
                temperature=0.3,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text
        except Exception as e:
            print(f"Anthropic summarization error: {e}")
            return None
    
    def _summarize_local(self, prompt):
        """Summarize using local LLM"""
        try:
            response = self.local_model(
                prompt,
                max_tokens=1500,
                temperature=0.3,
                stop=["User:", "Human:"]
            )
            return response['choices'][0]['text']
        except Exception as e:
            print(f"Local model summarization error: {e}")
            return None
    
    def _fallback_summary(self, transcript):
        """Fallback summary when no AI model is available"""
        words = transcript.split()
        word_count = len(words)
        
        # Simple extractive summary - first and last paragraphs
        paragraphs = transcript.split('\n\n')
        
        summary = f"""## Meeting Summary
        
**Word Count**: {word_count}

**Content Overview**:
{paragraphs[0] if paragraphs else transcript[:500]}

**Note**: This is a basic summary. Configure an AI model (OpenAI, Anthropic, or local) for detailed summaries.
"""
        return summary

