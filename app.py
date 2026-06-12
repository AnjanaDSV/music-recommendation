from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
from lastfm import get_recommendations, get_recommendations_v2, MOOD_DISPLAY
from ollama_client import analyze_mood, fallback_detect

load_dotenv()

app = Flask(__name__)

MOODS = ["Happy", "Sad", "Energetic", "Calm", "Focused", "Romantic", "Angry", "Melancholic"]
GENRES = ["Pop", "Rock", "Jazz", "Classical", "Hip-Hop", "Electronic", "R&B", "Indie", "Metal", "Country"]


@app.route("/")
def index():
    return render_template("index.html", moods=MOODS, genres=GENRES)


@app.route("/recommend", methods=["POST"])
def recommend():
    mood = request.form.get("mood", "happy").lower()
    genre = request.form.get("genre", "pop").lower()
    tracks = get_recommendations(genre, mood)
    return render_template(
        "results.html",
        tracks=tracks,
        mood=mood.capitalize(),
        genre=genre.capitalize(),
    )


@app.route("/v2")
def index_v2():
    return render_template("index_v2.html")


@app.route("/v2/recommend", methods=["POST"])
def recommend_v2():
    user_text = request.form.get("mood_text", "").strip()
    if not user_text:
        return redirect(url_for("index_v2"))

    ai_result, error = analyze_mood(user_text)

    ollama_down = False

    if error == "connection_error" or ai_result is None:
        ollama_down = True
        mood = fallback_detect(user_text)
        genre = "indie"
        vibe_label = f"{mood.capitalize()} Vibes"
        explanation = "AI engine unavailable — keyword-based fallback used."
        search_tags = None
    else:
        genre = ai_result.get("genre", "pop").lower()
        mood = ai_result.get("mood_tag", "calm").lower()
        vibe_label = ai_result.get("vibe_label", "Your Playlist")
        explanation = ai_result.get("explanation", "")
        search_tags = ai_result.get("search_tags", [])

    badge = MOOD_DISPLAY.get(mood, mood.capitalize())
    tracks = get_recommendations_v2(genre, mood, search_tags=search_tags)

    for track in tracks:
        track["mood_badge"] = badge

    return render_template(
        "results_v2.html",
        tracks=tracks,
        vibe_label=vibe_label,
        explanation=explanation,
        genre=genre.capitalize(),
        mood=mood.capitalize(),
        ollama_down=ollama_down,
    )


if __name__ == "__main__":
    app.run(debug=True)
