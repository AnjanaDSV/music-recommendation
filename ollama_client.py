import json
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3"

SYSTEM_PROMPT = (
    "You are a music recommendation assistant. "
    "Analyze the user's mood description and return a JSON object with exactly these fields:\n"
    "{\n"
    '  "genre": "one of: pop, rock, jazz, classical, hip-hop, electronic, indie, r&b",\n'
    '  "mood_tag": "one of: happy, sad, energetic, calm, focused, romantic, angry, melancholic",\n'
    '  "search_tags": ["tag1", "tag2", "tag3"],\n'
    '  "explanation": "one sentence explaining why these recommendations fit the user mood",\n'
    '  "vibe_label": "a 2-3 word label for this mood e.g. Late Night Chill"\n'
    "}\n"
    "Return ONLY valid JSON, no other text."
)

_MOOD_KEYWORDS = {
    "happy":      ["happy", "joy", "joyful", "excited", "cheerful", "good", "great", "fun", "upbeat", "smile"],
    "sad":        ["sad", "cry", "crying", "depressed", "down", "blue", "miss", "lonely", "heartbreak", "grief"],
    "energetic":  ["energetic", "pump", "workout", "running", "hype", "active", "dance", "party", "gym"],
    "calm":       ["calm", "chill", "relax", "tired", "slow", "peaceful", "quiet", "gentle", "rest", "cooking", "evening", "wind down"],
    "focused":    ["focus", "focused", "study", "work", "concentrate", "productive", "reading", "writing"],
    "romantic":   ["romantic", "love", "date", "dinner", "cozy", "candlelight", "valentine"],
    "angry":      ["angry", "mad", "frustrated", "rage", "furious", "annoyed", "stress", "stressed"],
    "melancholic": ["melancholic", "nostalgic", "memories", "dreamy", "wistful", "bittersweet", "miss"],
}


def _extract_json(text):
    text = text.strip()
    start = text.find("{")
    end = text.rfind("}") + 1
    if start != -1 and end > start:
        return json.loads(text[start:end])
    return json.loads(text)


def fallback_detect(text):
    text_lower = text.lower()
    words = text_lower.split()
    for word in words:
        for mood, keywords in _MOOD_KEYWORDS.items():
            if word in keywords:
                return mood
    for mood, keywords in _MOOD_KEYWORDS.items():
        if any(kw in text_lower for kw in keywords):
            return mood
    return "calm"


def analyze_mood(user_text):
    try:
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": user_text,
            "system": SYSTEM_PROMPT,
            "stream": False,
        }
        resp = requests.post(OLLAMA_URL, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        raw = data.get("response", "")
        result = _extract_json(raw)
        return result, None
    except requests.exceptions.ConnectionError:
        return None, "connection_error"
    except (json.JSONDecodeError, KeyError):
        return None, "parse_error"
    except Exception as e:
        return None, str(e)
