from fastapi import APIRouter, BackgroundTasks, HTTPException
from models.song import SongRequest, SongResponse, SongStatus
from services.lyrics_service import LyricsService
from services.voice_service import VoiceService
from services.beat_service import BeatService
from services.audio_service import AudioService
import uuid
import time

router = APIRouter()

lyrics_service = LyricsService()
voice_service = VoiceService()
beat_service = BeatService()
audio_service = AudioService()

# In-memory store for MVP
jobs = {}

async def process_song_generation(job_id: str, request: SongRequest):
    jobs[job_id]["status"] = "processing"
    
    try:
        # 1. Generate Lyrics
        lyrics = await lyrics_service.generate_lyrics(request.topic, request.mood, request.energy)
        jobs[job_id]["lyrics"] = lyrics
        jobs[job_id]["progress"] = 30
        
        # 2. Synthesize Vocals
        # Combine all lyrics sections into one text for TTS
        lyrics_text = "\n\n".join([
            f"{section['text']}" 
            for section in lyrics.get("lyrics", [])
        ])
        
        vocals_path = await voice_service.synthesize(lyrics_text, output_dir="output/vocals")
        jobs[job_id]["vocals_path"] = vocals_path
        jobs[job_id]["progress"] = 50
        
        # 3. Get Beat
        beat_path = await beat_service.get_beat(request.bpm, request.mood)
        jobs[job_id]["beat_path"] = beat_path
        jobs[job_id]["progress"] = 70
        
        # 4. Mix Audio
        final_path = await audio_service.mix_song(vocals_path, beat_path, f"output/songs/{job_id}.mp3")
        jobs[job_id]["final_path"] = final_path
        jobs[job_id]["progress"] = 90
        
        jobs[job_id]["status"] = "completed"
        jobs[job_id]["progress"] = 100
        jobs[job_id]["result_url"] = f"/output/songs/{job_id}.mp3"
        
    except Exception as e:
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)
        print(f"Job {job_id} failed: {e}")

@router.post("/generate", response_model=SongResponse)
async def generate_song(request: SongRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    jobs[job_id] = {
        "job_id": job_id,
        "status": "pending",
        "progress": 0,
        "created_at": time.time()
    }
    
    background_tasks.add_task(process_song_generation, job_id, request)
    
    return SongResponse(
        job_id=job_id,
        status="pending",
        estimated_time=60
    )

@router.get("/{job_id}/status", response_model=SongStatus)
async def get_song_status(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return SongStatus(**jobs[job_id])
