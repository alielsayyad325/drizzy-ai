from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from api import songs
import os

app = FastAPI(title="Drizzy AI API", version="0.1.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for serving generated audio
output_dir = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(output_dir, exist_ok=True)
app.mount("/output", StaticFiles(directory=output_dir), name="output")

# Include Routers
app.include_router(songs.router, prefix="/api/v1/songs", tags=["songs"])

@app.get("/")
async def root():
    return {"message": "Drizzy AI Music Generation API is running"}
