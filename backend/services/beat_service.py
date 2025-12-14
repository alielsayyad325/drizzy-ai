import os
import json
from typing import Optional

class BeatService:
    def __init__(self, beats_dir: str = "assets/beats"):
        self.beats_dir = beats_dir
        self.beats_catalog = self._load_catalog()

    def _load_catalog(self) -> list:
        """Load beat catalog from JSON file or return default catalog."""
        catalog_path = os.path.join(self.beats_dir, "catalog.json")
        
        if os.path.exists(catalog_path):
            with open(catalog_path, 'r') as f:
                return json.load(f)
        
        # Default catalog (will be populated when we add beats)
        return []

    async def get_beat(self, bpm: int, mood: str) -> Optional[str]:
        """
        Selects a beat from the library based on BPM and mood.
        Returns the path to the beat file.
        """
        # For MVP, we'll use a simple matching algorithm
        # In V2, this could be more sophisticated
        
        if not self.beats_catalog:
            print("Warning: No beats in catalog. Using mock beat.")
            return self._create_mock_beat()
        
        # Find beats that match the criteria
        matching_beats = [
            beat for beat in self.beats_catalog
            if abs(beat.get("bpm", 0) - bpm) <= 10  # Within 10 BPM
            and beat.get("mood", "").lower() == mood.lower()
        ]
        
        if not matching_beats:
            # Fallback: just match BPM
            matching_beats = [
                beat for beat in self.beats_catalog
                if abs(beat.get("bpm", 0) - bpm) <= 20
            ]
        
        if not matching_beats:
            # Use first available beat
            matching_beats = self.beats_catalog
        
        if matching_beats:
            selected_beat = matching_beats[0]
            beat_path = os.path.join(self.beats_dir, selected_beat["file"])
            print(f"Selected beat: {selected_beat['name']} (BPM: {selected_beat['bpm']}, Mood: {selected_beat['mood']})")
            return beat_path
        
        return self._create_mock_beat()

    def _create_mock_beat(self) -> str:
        """Creates a mock beat file for testing."""
        os.makedirs(self.beats_dir, exist_ok=True)
        mock_path = os.path.join(self.beats_dir, "mock_beat.mp3")
        
        if not os.path.exists(mock_path):
            with open(mock_path, 'w') as f:
                f.write("Mock beat content")
        
        print(f"Using mock beat at {mock_path}")
        return mock_path
