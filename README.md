# Drizzy AI - Automated Music Generation MVP

## Overview
Drizzy AI is a fully automated music generation system designed to create original rap and melodic hip-hop songs. It orchestrates a pipeline of AI models to generate lyrics, synthesize vocals, select beats, and mix the final audio track.

**Note:** This system is designed to generate *original* content and does not clone specific artists.

## Architecture
The system consists of:
- **Frontend**: Next.js (React) for user interaction.
- **Backend**: FastAPI (Python) for orchestration and processing.
- **AI Pipeline**:
    - **Lyrics**: LLM (GPT-4o/Claude)
    - **Vocals**: TTS/SVC (ElevenLabs/Custom)
    - **Audio**: FFmpeg/Python for mixing.

## Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- FFmpeg installed on system path.
- API Keys for OpenAI, ElevenLabs (or equivalent).

### Installation

1.  **Backend Setup**
    ```bash
    cd backend
    pip install -r requirements.txt
    uvicorn main:app --reload
    ```

2.  **Frontend Setup**
    ```bash
    cd frontend
    npm install
    npm run dev
    ```

## Documentation
See [DESIGN.md](./DESIGN.md) for detailed architecture, API design, and roadmap.
