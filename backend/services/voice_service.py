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
        self.api_key = os.getenv("ELEVENLABS_API_KEY")
        # Default Voice ID (e.g., "Adam" or similar generic voice)
        # Using a standard ElevenLabs voice ID (e.g., "Rachel" or "Josh")
        # "flq6f7yk4E4fJM5XTYuZ" is Michael (Smooth/Deep Male)
        self.voice_id = "flq6f7yk4E4fJM5XTYuZ" 
        self.chunk_size = 1024

    async def synthesize(self, text: str, output_dir: str = "output") -> str:
        """
        Converts text to speech and saves to file.
        Returns the path to the saved audio file.
        """
        if not self.api_key:
            raise ValueError("ELEVENLABS_API_KEY not found in environment variables.")

        url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}"
        
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.api_key
        }
        
        data = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75
            }
        }

        print(f"Synthesizing audio for text: {text[:50]}...")
        
        try:
            response = requests.post(url, json=data, headers=headers)
            
            if response.status_code != 200:
                error_msg = f"ElevenLabs API Error: {response.status_code} - {response.text}"
                print(error_msg)
                raise Exception(error_msg)

            # Ensure output directory exists
            os.makedirs(output_dir, exist_ok=True)
            
            filename = f"{uuid.uuid4()}.mp3"
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=self.chunk_size):
                    if chunk:
                        f.write(chunk)
            
            print(f"Audio saved to {filepath}")
            return filepath

        except Exception as e:
            print(f"Exception in voice synthesis: {e}")
            raise e
