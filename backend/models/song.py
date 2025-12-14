from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from enum import Enum
import uuid

class Mood(str, Enum):
    HYPE = "hype"
    CHILL = "chill"
    SAD = "sad"
    AGGRESSIVE = "aggressive"
    ROMANTIC = "romantic"

class SongRequest(BaseModel):
    topic: str
    mood: Mood
    bpm: Optional[int] = 140
    energy: str = "high" # low, medium, high

class SongResponse(BaseModel):
    job_id: str
    status: str
    estimated_time: int

class SongStatus(BaseModel):
    job_id: str
    status: str
    progress: int
    result_url: Optional[str] = None
    lyrics: Optional[Dict[str, Any]] = None
