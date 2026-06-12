from flask import Flask, render_template, request
from dotenv import load_dotenv
from lastfm import get_recommendations

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


if __name__ == "__main__":
    app.run(debug=True)
