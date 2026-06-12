import os
import requests
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv

load_dotenv()

LASTFM_API_KEY = os.getenv("LASTFM_API_KEY")
BASE_URL = "https://ws.audioscrobbler.com/2.0/"

MOOD_TAGS = {
    "happy": ["happy", "feel-good", "upbeat"],
    "sad": ["sad", "melancholic", "heartbreak"],
    "energetic": ["energetic", "workout", "pump-up"],
    "calm": ["chill", "relaxing", "ambient"],
    "focused": ["instrumental", "focus", "study"],
    "romantic": ["romantic", "love", "slow"],
    "angry": ["aggressive", "intense", "heavy"],
    "melancholic": ["melancholic", "dreamy", "nostalgic"],
}

MOOD_DISPLAY = {
    "happy": "Feel Good",
    "sad": "Emotional",
    "energetic": "High Energy",
    "calm": "Chill Vibes",
    "focused": "Deep Focus",
    "romantic": "Romantic",
    "angry": "Intense",
    "melancholic": "Nostalgic",
}


def _best_image(images):
    for size in ("extralarge", "large", "medium", "small"):
        for img in images:
            if img.get("size") == size and img.get("#text"):
                return img["#text"]
    return ""


def _fetch(params):
    try:
        params["api_key"] = LASTFM_API_KEY
        params["format"] = "json"
        r = requests.get(BASE_URL, params=params, timeout=10)
        return r.json()
    except Exception:
        return {}


def _tag_tracks(tag, limit=50):
    data = _fetch({"method": "tag.gettoptracks", "tag": tag, "limit": limit})
    return data.get("tracks", {}).get("track", [])


def _enrich_track(raw_track):
    artist = raw_track["artist"]["name"]
    name = raw_track["name"]

    data = _fetch({"method": "track.getinfo", "artist": artist, "track": name})
    info = data.get("track", {})

    image_url = ""
    if info:
        album = info.get("album", {})
        if album:
            image_url = _best_image(album.get("image", []))

    if not image_url:
        image_url = _best_image(raw_track.get("image", []))

    try:
        playcount = int(info.get("playcount", 0))
    except (ValueError, TypeError):
        playcount = 0

    return {
        "name": name,
        "artist": artist,
        "image_url": image_url,
        "playcount": f"{playcount:,}" if playcount else "N/A",
        "url": info.get("url") or raw_track.get("url", "#"),
    }


def get_recommendations_v2(genre, mood_tag, search_tags=None, limit=8):
    genre_tracks = _tag_tracks(genre)

    # Use Ollama's search_tags if provided; fall back to MOOD_TAGS mapping
    tags = search_tags if search_tags else MOOD_TAGS.get(mood_tag, [mood_tag])
    mood_keys = set()
    for tag in tags[:2]:
        for t in _tag_tracks(tag, limit=50):
            mood_keys.add((t["name"].lower(), t["artist"]["name"].lower()))

    seen = set()
    matched, unmatched = [], []
    for track in genre_tracks:
        key = (track["name"].lower(), track["artist"]["name"].lower())
        if key in seen:
            continue
        seen.add(key)
        if key in mood_keys:
            matched.append(track)
        else:
            unmatched.append(track)

    candidates = (matched + unmatched)[:limit]

    with ThreadPoolExecutor(max_workers=8) as ex:
        enriched = list(ex.map(_enrich_track, candidates))

    return enriched


def get_recommendations(genre, mood, limit=8):
    genre_tracks = _tag_tracks(genre)

    mood_tag = MOOD_TAGS.get(mood, [mood])[0]
    mood_keys = {
        (t["name"].lower(), t["artist"]["name"].lower())
        for t in _tag_tracks(mood_tag)
    }

    badge = MOOD_DISPLAY.get(mood, mood.capitalize())

    seen = set()
    matched, unmatched = [], []
    for track in genre_tracks:
        key = (track["name"].lower(), track["artist"]["name"].lower())
        if key in seen:
            continue
        seen.add(key)
        if key in mood_keys:
            matched.append(track)
        else:
            unmatched.append(track)

    candidates = (matched + unmatched)[:limit]

    with ThreadPoolExecutor(max_workers=8) as ex:
        enriched = list(ex.map(_enrich_track, candidates))

    for track in enriched:
        track["mood_badge"] = badge

    return enriched
