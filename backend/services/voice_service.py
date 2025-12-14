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
            print("Warning: ELEVENLABS_API_KEY not found.")
            # Return a mock file for testing if no key
            return self._generate_mock_audio(output_dir)

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
                with open("debug_voice.log", "a") as log:
                    log.write(f"Error from ElevenLabs: {response.text}\nStatus Code: {response.status_code}\n")
                print(f"Error from ElevenLabs: {response.text}")
                return self._generate_mock_audio(output_dir)

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
            with open("debug_voice.log", "a") as log:
                log.write(f"Exception in voice synthesis: {e}\n")
            print(f"Exception in voice synthesis: {e}")
            return self._generate_mock_audio(output_dir)

    def _generate_mock_audio(self, output_dir: str) -> str:
        """Generates a silent or dummy file for testing."""
        os.makedirs(output_dir, exist_ok=True)
        filename = f"mock_{uuid.uuid4()}.mp3"
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w') as f:
            f.write("Mock audio content")
        print(f"Generated mock audio at {filepath}")
        return filepath
