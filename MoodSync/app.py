from flask import Flask, render_template, request, redirect, url_for
from recommendation_model import recommend_songs
from data_processing import load_and_prepare_data
from spotify_utils import get_spotify_track_id, get_spotify_url
import time  # For performance measurement
import random  # For random sampling

app = Flask(__name__)

# Load data globally to avoid reloading on every request
try:
    df, _ = load_and_prepare_data()
    print("Data successfully loaded.")
except Exception as e:
    print(f"Error loading data during initialization: {e}")
    df = None  # Handle failure gracefully

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        mood = request.form.get('mood', '').strip().lower()  # Get user mood input and normalize
        if not mood:
            return render_template('index.html', error="Please select a valid mood.")  # Handle invalid input

        print(f"User selected mood: {mood}")  # Debugging

        # Start timing the recommendation process
        start_time = time.time()

        # Recommend songs based on mood
        try:
            recommended_songs = recommend_songs_based_on_mood(mood)
        except Exception as e:
            print(f"Error in recommendation logic: {e}")
            return render_template('index.html', error="An error occurred while generating recommendations.")

        # Limit to top 50 recommendations or less, depending on availability
        recommended_songs = recommended_songs[:50]

        # Add Spotify URLs to recommendations
        recommended_songs_with_spotify = []
        for song in recommended_songs:
            try:
                track_id = get_spotify_track_id(song[0])  # Get Spotify track ID
                if track_id:
                    spotify_url = get_spotify_url(track_id)  # Get Spotify URL
                    recommended_songs_with_spotify.append({
                        'name': song[0],
                        'spotify_url': spotify_url
                    })
                else:
                    print(f"Spotify track ID not found for: {song[0]}")
            except Exception as e:
                print(f"Error fetching Spotify URL for song {song[0]}: {e}")

        end_time = time.time()
        print(f"Recommendation generation and Spotify URL fetching took {end_time - start_time:.2f} seconds")

        # Render recommendations page
        return render_template('recommendation.html', recommendations=recommended_songs_with_spotify)

    return render_template('index.html')


def recommend_songs_based_on_mood(mood):
    """
    Recommends a diverse set of songs based on the user's mood.
    """
    global df  # Use globally loaded data

    if df is None:
        print("Data is not loaded.")
        return []

    # Define mood-to-genre mapping
    mood_to_genre = {
        "happy": ["Bollywooddance", "BollywoodMotivational"],
        "sad": ["BollywoodSad", "bollywoodromanticsad"],
        "romantic": ["bollywoodromantic"],
        "energetic": ["Bollywooddance", "BollywoodMotivational"],
        "relaxed": ["bollywoodromanticsad", "BollywoodSad"],
    }

    # Check if the mood is valid
    if mood not in mood_to_genre:
        print(f"Invalid mood: {mood}")
        return []

    # Filter songs based on genres for the selected mood
    recommended_genres = mood_to_genre[mood]
    try:
        filtered_songs = df[df["Genre"].str.lower().isin([genre.lower() for genre in recommended_genres])]
        
        # Shuffle and select 50 songs randomly if more than 50 are available
        all_songs = filtered_songs[["Song-Name", "Singer/Artists", "Genre"]].values.tolist()
        if len(all_songs) > 20:
            recommended_songs = random.sample(all_songs, 20)
        else:
            recommended_songs = all_songs  # If fewer than 50 songs exist, return all
    except Exception as e:
        print(f"Error during song filtering: {e}")
        return []

    return recommended_songs


if __name__ == '__main__':
    app.run(debug=True)
