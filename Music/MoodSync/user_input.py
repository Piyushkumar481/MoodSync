import pandas as pd

DATASET_PATH = "datasets/Songs.csv"

def get_user_mood():
    """
    Collects user's mood and recommends songs based on it.
    """
    print("\nEnter your current mood.")

    mood = input("Enter your mood (e.g., happy, sad, romantic, energetic, relaxed): ").strip().lower()
    return mood


def recommend_songs_based_on_mood(mood):
    """
    Recommends songs based on the user's mood.
    Matches the mood to the Bollywood genre and recommends songs from the dataset.
    """
    # Load the dataset
    try:
        df = pd.read_csv(DATASET_PATH)
    except FileNotFoundError:
        print("\nNo dataset found. Please add songs first.")
        return []

    # Define mood-to-genre mapping for Bollywood music
    mood_to_genre = {
        "happy": ["Bollywooddance", "BollywoodMotivational"],
        "sad": ["BollywoodSad", "bollywoodromanticsad"],
        "romantic": ["bollywoodromantic"],
        "energetic": ["Bollywooddance", "BollywoodMotivational"],
        "relaxed": ["bollywoodromanticsad", "BollywoodSad"],
    }

    # Check if mood exists in the mapping
    if mood not in mood_to_genre:
        print("\nSorry, mood not recognized. Try again with a valid mood (e.g., happy, sad, romantic, energetic, relaxed).")
        return []

    # Get the list of genres associated with the user's mood
    recommended_genres = mood_to_genre[mood]

    # Filter songs by genres that match the mood
    recommended_songs = df[df["Genre"].str.lower().isin([genre.lower() for genre in recommended_genres])]

    if recommended_songs.empty:
        print("\nNo matching songs found for your mood.")
        return []

    # Sort by user rating and recommend top songs
    recommended_songs = recommended_songs.sort_values(by="User-Rating", ascending=False)

    # Return song recommendations (song name, artist, genre)
    return recommended_songs[["Song-Name", "Singer/Artists", "Genre"]].values.tolist()
