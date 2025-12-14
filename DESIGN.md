# AI Music Generation MVP - Design Document

## 1. System Architecture

### High-Level Architecture Diagram
```mermaid
graph TD
    User[User Client (Web/Mobile)] -->|Request (Topic, Mood, BPM)| API_Gateway[API Gateway / Load Balancer]
    API_Gateway -->|HTTP/REST| Backend[Backend Service (FastAPI)]
    
    subgraph "Core Pipeline"
        Backend -->|1. Generate Lyrics| LLM_Service[LLM Service (GPT-4o/Claude 3.5)]
        Backend -->|2. Synthesize Vocals| TTS_Service[Voice Synthesis Engine]
        Backend -->|3. Get Beat| Beat_Service[Beat Library / Generator]
        Backend -->|4. Mix & Master| Audio_Engine[Audio Processing Engine (FFmpeg/Python)]
    end
    
    subgraph "Data & Storage"
        Backend -->|Store Metadata| DB[(PostgreSQL)]
        Backend -->|Store Audio Files| Object_Store[(S3 / Cloud Storage)]
        Beat_Service -->|Retrieve| Beat_Library[(Beat Library)]
    end
    
    Backend -->|Return Final Audio URL| API_Gateway
    API_Gateway -->|Stream/Download| User
```

### Modular Pipeline Breakdown
The system is divided into 4 distinct stages, orchestrated by the Backend Service:

1.  **Lyrics Generation Module**:
    *   **Input**: Topic, Mood, Energy.
    *   **Process**: Prompt Engineering -> LLM -> Structured JSON Output.
    *   **Output**: Lyrics with timing markers/structure (Verse, Hook, etc.).

2.  **Voice Synthesis Module**:
    *   **Input**: Lyrics text, Voice ID, Style/Emotion.
    *   **Process**: Text-to-Speech / Singing-Voice-Conversion.
    *   **Output**: Raw vocal stems (WAV).

3.  **Beat Module**:
    *   **Input**: BPM, Mood, Genre.
    *   **Process**: Database Query (MVP) or Generative Audio Model (V2).
    *   **Output**: Instrumental track (WAV/MP3) + Beat Grid/Timing info.

4.  **Audio Processing Module**:
    *   **Input**: Vocal Stems, Instrumental, Timing Data.
    *   **Process**: Time-stretching, Pitch correction (Auto-tune), EQ, Compression, Mixing.
    *   **Output**: Final Mastered Song (MP3/WAV).

---

## 2. API Layer Design

### REST API Endpoints

#### `POST /api/v1/songs/generate`
Initiates the song generation process.
**Request Payload:**
```json
{
  "topic": "Coding late at night",
  "mood": "focused",
  "bpm": 140,
  "energy": "high",
  "genre": "trap"
}
```
**Response:**
```json
{
  "job_id": "song_12345",
  "status": "processing",
  "estimated_time": 60
}
```

#### `GET /api/v1/songs/{job_id}/status`
Polls for the status of the generation.
**Response:**
```json
{
  "job_id": "song_12345",
  "status": "completed", 
  "progress": 100,
  "result_url": "https://cdn.drizzy-ai.com/songs/song_12345.mp3",
  "lyrics": { ... }
}
```

#### `GET /api/v1/beats`
List available beats (for manual selection if supported).

---

## 3. Model Selection Strategy

### Lyrics Generation
*   **Primary**: **GPT-4o** or **Claude 3.5 Sonnet**.
*   **Reasoning**: Best-in-class instruction following for strict JSON structure and rhyming schemes.
*   **Fallback**: Llama 3 (70B) for lower cost/latency if needed.

### Voice Synthesis
*   **MVP**: **ElevenLabs** (using "Speech to Speech" or high-expressivity TTS) or **Suno/Udio API** (if available/legal for stems).
*   **Alternative**: **Bark** (Open Source) or **RVC (Retrieval-based Voice Conversion)**.
*   **Recommendation for MVP**: Use a high-quality commercial API (ElevenLabs) for the "Voice" to ensure quality, or RVC over a TTS base for specific "flow".
*   *Constraint Check*: Must be original. We will use generic voice models, not celebrity clones.

### Beat Generation
*   **MVP**: **Pre-curated Library**. High quality, royalty-free beats tagged by BPM/Mood. Reliable and cheap.
*   **V2**: **MusicGen** (Meta) or **Stable Audio**.

---

## 4. Database Schema (PostgreSQL)

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE,
    created_at TIMESTAMP
);

CREATE TABLE songs (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    title VARCHAR(255),
    topic TEXT,
    mood VARCHAR(50),
    bpm INTEGER,
    status VARCHAR(20), -- 'pending', 'processing', 'completed', 'failed'
    lyrics_json JSONB,
    audio_url TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE beats (
    id UUID PRIMARY KEY,
    name VARCHAR(255),
    bpm INTEGER,
    mood VARCHAR(50),
    file_url TEXT,
    duration_seconds INTEGER
);
```

---

## 5. Frontend + Backend Separation

*   **Frontend**: **Next.js (React)**.
    *   Hosted on Vercel.
    *   Responsible for UI, Form Input, Audio Player, Visualization.
*   **Backend**: **FastAPI (Python)**.
    *   Hosted on AWS EC2 / Google Cloud Run.
    *   Handles orchestration, GPU model inference (if self-hosted) or API calls.
    *   Uses **Celery / Redis** for async task queue (song generation takes time).

---

## 6. Security & Performance

*   **Security**:
    *   Rate Limiting (Redis) to prevent abuse of expensive APIs.
    *   Input Validation (Pydantic) to prevent injection.
    *   Signed URLs (S3) for private audio access.
*   **Performance**:
    *   **Async Processing**: The generation pipeline is long (30s-2m). API must be non-blocking.
    *   **Caching**: Cache generated lyrics or beats if re-used.
    *   **CDN**: Serve audio files via CloudFront/CDN.

---

## 7. Prompt Templates

### Lyrics Generation Prompt (System Prompt)
```text
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
{
  "title": "Song Title",
  "bpm_suggestion": 140,
  "lyrics": [
    { "section": "Intro", "text": "..." },
    { "section": "Verse 1", "text": "..." },
    { "section": "Hook", "text": "..." },
    ...
  ]
}
```

### Vocal Synthesis Control
*   **Voice ID**: Generic Male/Female (e.g., "Adam" or "Bella" from standard libraries).
*   **Stability**: 0.5 (Variable for more emotion).
*   **Similarity Boost**: 0.75.

---

## 8. Roadmap

### Phase 1: MVP (Weeks 1-2)
*   [ ] Set up FastAPI Backend & Next.js Frontend.
*   [ ] Implement Lyrics Generation (OpenAI API).
*   [ ] Implement Basic TTS (ElevenLabs/OpenAI Audio).
*   [ ] Create "Beat Library" (5-10 local MP3s).
*   [ ] Build "Stitching" logic (Overlay vocals on beat using FFmpeg).
*   [ ] Basic UI to input topic and play result.

### Phase 2: Enhanced V1 (Weeks 3-4)
*   [ ] Beat Selection Logic (Match BPM/Mood).
*   [ ] Vocal Timing/Alignment (Time-stretching vocals to match beat).
*   [ ] User Accounts & History.
*   [ ] Download/Export functionality.

### Phase 3: V2 Upgrade (Future)
*   [ ] Generative Beats (MusicGen).
*   [ ] Advanced Mixing (Auto-tune, EQ, Reverb chains).
*   [ ] Multi-voice support (Features).
*   [ ] Video generation (Music Video).


