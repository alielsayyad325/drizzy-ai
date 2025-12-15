import os
import requests
import uuid
from dotenv import load_dotenv
from pathlib import Path

# Load .env from backend directory
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

class VoiceService:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            print("Warning: OPENAI_API_KEY not found in environment variables.")
        
        # Initialize OpenAI Client
        from openai import OpenAI
        self.client = OpenAI(api_key=self.api_key)
        
        # OpenAI Voice settings
        # "onyx" is a deep male voice, good for rap/hiphop style
        self.voice = "onyx" 
        self.model = "tts-1" # tts-1 is faster (good for real-time), tts-1-hd is higher quality

    async def synthesize(self, text: str, output_dir: str = "output") -> str:
        """
        Converts text to speech using OpenAI API and saves to file.
        Returns the path to the saved audio file.
        """
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables.")

        print(f"Synthesizing audio for text (OpenAI): {text[:50]}...")
        
        try:
            response = self.client.audio.speech.create(
                model=self.model,
                voice=self.voice,
                input=text
            )
            
            # Ensure output directory exists
            os.makedirs(output_dir, exist_ok=True)
            
            filename = f"{uuid.uuid4()}.mp3"
            filepath = os.path.join(output_dir, filename)
            
            # Save the binary content
            response.stream_to_file(filepath)
            
            print(f"Audio saved to {filepath}")
            return filepath

        except Exception as e:
            print(f"Exception in voice synthesis: {e}")
            raise e
