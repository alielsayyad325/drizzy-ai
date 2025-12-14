import json
import os
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path

# Load .env from backend directory
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

class LyricsService:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("Warning: OPENAI_API_KEY not found in environment variables.")
        self.client = OpenAI(api_key=api_key)

    async def generate_lyrics(self, topic: str, mood: str, energy: str) -> dict:
        """
        Generates structured lyrics using an LLM.
        """
        system_prompt = f"""
You are a professional hip-hop songwriter and ghostwriter. Your goal is to write original, rhythmic, and structured rap lyrics based on the user's topic and mood.

**Constraints:**
1.  Structure MUST be: Intro -> Verse 1 -> Hook -> Verse 2 -> Bridge -> Hook -> Outro.
2.  Do NOT use the name of any real artist.
3.  Output MUST be valid JSON.
4.  Include a "bpm_suggestion" and "key_suggestion".
5.  Lyrics should be rhythmic, using internal rhymes and flow patterns suitable for a {energy} energy beat.

**Input:**
Topic: {topic}
Mood: {mood}

**Output Format (JSON Only):**
{{
  "title": "Song Title",
  "bpm_suggestion": 140,
  "key_suggestion": "C Minor",
  "lyrics": [
    {{ "section": "Intro", "text": "..." }},
    {{ "section": "Verse 1", "text": "..." }},
    {{ "section": "Hook", "text": "..." }},
    ...
  ]
}}
"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Topic: {topic}\nMood: {mood}"}
                ],
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
            
        except Exception as e:
            print(f"Error generating lyrics: {e}")
            print(f"Error type: {type(e).__name__}")
            print(f"API Key present: {bool(self.client.api_key)}")
            print(f"API Key starts with: {self.client.api_key[:10] if self.client.api_key else 'None'}...")
            # Fallback mock for testing if API fails or no key
            return {
                "title": f"Error: {topic}",
                "bpm_suggestion": 140,
                "lyrics": [
                    {"section": "Error", "text": f"Could not generate lyrics. Check API Key. Error: {str(e)}"}
                ]
            }
