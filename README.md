# MoodTunes — Music Recommendation App

Discover music curated to your current mood and genre preference, powered by the Last.fm API.

## Version History

| Version | Description |
|---------|-------------|
| v1.0 | Traditional recommendation engine (Flask + Last.fm API, rule-based mood-to-tag mapping) |
| v2.0 | Coming soon: LLM-powered mood understanding via Ollama |

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

### 4. Configure your API key

```bash
cp .env.example .env
```

Edit `.env` and replace `your-key-here` with your Last.fm API key.  
Get a free key at: https://www.last.fm/api/account/create

### 5. Run the app

```bash
python app.py
```

Open your browser at **http://localhost:5000**

---

## How It Works

MoodTunes uses a **mood-to-tag mapping system** to find music that fits both your chosen genre and emotional state.

### Mood → Tag Mapping

Each mood maps to a set of Last.fm tags that describe that emotional quality:

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

### Recommendation Process

1. Fetches top 50 tracks for the selected **genre** tag from Last.fm
2. Fetches top 50 tracks for the primary **mood** tag
3. Tracks appearing in both lists are **prioritized** (genre × mood intersection)
4. The top 8 candidates are enriched via `track.getInfo` to fetch album art and play counts
5. Results are displayed in a card grid with a mood badge, album art, and a direct Last.fm link

---

## Tech Stack

- **Backend** — Python + Flask
- **API** — Last.fm Web API (`tag.getTopTracks`, `track.getInfo`)
- **Frontend** — Vanilla HTML / CSS, dark theme with `#1db954` green accent
- **Env management** — python-dotenv

---

## Screenshots

*Coming soon*
