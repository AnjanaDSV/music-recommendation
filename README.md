# MoodTunes — Music Recommendation App

Discover music curated to your current mood and genre preference.  
V1 uses dropdowns + rule-based logic. V2 uses a local LLM to understand free-text mood descriptions.

## Version History

| Version | Description |
|---------|-------------|
| v1.0 | Traditional recommendation engine (Flask + Last.fm API, dropdown-based) |
| v2.0 | LLM-powered mood understanding (Ollama + Llama3 local inference, natural language input, AI-generated explanations, zero API costs, fully offline LLM) |

---

## Why Two Versions?

V1 demonstrates traditional rule-based recommendation systems. V2 shows how the same problem can be solved with local LLM inference — same Last.fm data source, completely different intelligence layer. The upgrade isolates exactly what LLMs add: natural language understanding and contextual explanation.

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/AnjanaDSV/music-recommendation.git
cd music-recommendation
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your Last.fm API key

```bash
cp .env.example .env
```

Edit `.env` and replace `your-key-here` with your Last.fm API key.  
Get a free key at: https://www.last.fm/api/account/create

### 5. (V2 only) Install Ollama + Llama3

Install Ollama from https://ollama.com, then pull the model:

```bash
ollama pull llama3
ollama serve
```

### 6. Run the app

```bash
python app.py
```

Open your browser at **http://localhost:5000**  
V2 interface is at **http://localhost:5000/v2**

---

## How It Works

### V1 — Rule-Based

1. User selects a **mood** and **genre** from dropdowns
2. The app fetches top 50 tracks for the genre tag from Last.fm
3. It also fetches top 50 tracks for the primary mood tag
4. Tracks in both lists (genre × mood intersection) are prioritised
5. Top 8 are enriched via `track.getInfo` for album art and play counts

#### Mood → Tag Mapping

| Mood | Tags Used |
|------|-----------|
| Happy | happy, feel-good, upbeat |
| Sad | sad, melancholic, heartbreak |
| Energetic | energetic, workout, pump-up |
| Calm | chill, relaxing, ambient |
| Focused | instrumental, focus, study |
| Romantic | romantic, love, slow |
| Angry | aggressive, intense, heavy |
| Melancholic | melancholic, dreamy, nostalgic |

### V2 — LLM-Powered

1. User types a free-text mood description (e.g. *"tired after a long day, cooking dinner"*)
2. The text is sent to a local **Llama3** model via Ollama
3. Llama3 returns a JSON object with: `genre`, `mood_tag`, `search_tags`, `explanation`, `vibe_label`
4. The app uses `genre + search_tags` to query Last.fm (same API layer as V1)
5. Results include the AI's explanation and a custom vibe label

If Ollama is not running, V2 gracefully falls back to keyword-based mood detection.

---

## Tech Stack

- **Backend** — Python + Flask
- **V1 intelligence** — Rule-based mood-to-tag mapping
- **V2 intelligence** — Ollama + Llama3 (local inference, fully offline)
- **Music data** — Last.fm Web API (`tag.getTopTracks`, `track.getInfo`)
- **Frontend** — Vanilla HTML / CSS, dark theme with `#1db954` green accent
- **Env management** — python-dotenv

---

## Screenshots

*Coming soon*
