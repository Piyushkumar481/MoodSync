from user_input import get_user_mood
from data_processing import load_and_prepare_data
from recommendation_model import build_similarity_matrix, recommend_songs

def main():
    # Load data and prepare
    df, le = load_and_prepare_data()
    
    if df.empty:
        print("No songs available to recommend. Please add some songs.")
        return

    # Get user mood input
    print("Please enter your mood and activity:")
    user_mood = get_user_mood()

    # Filter songs based on mood or activity (optional step)
    # This step can be customized based on how you want to filter songs according to the user's input
    # For example, filter songs by genre or mood
    mood_filtered_df = df[df['Genre'].str.contains(user_mood, case=False, na=False)]
    
    # Display filtered songs if there are any
    if not mood_filtered_df.empty:
        print(f"Songs matching your mood '{user_mood}':")
        for i, song in enumerate(mood_filtered_df['Song-Name']):
            print(f"{i}. {song}")
    else:
        print(f"No songs found for the mood '{user_mood}'. Using the full list of songs.")
        mood_filtered_df = df  # Use the full dataset if no matching songs found

    # Ask user to select a song for recommendations
    song_index = int(input("Enter the song index for recommendations: "))
    
    if song_index < 0 or song_index >= len(mood_filtered_df):
        print("Invalid song index. Exiting.")
        return
    
    # Build similarity matrix
    similarity_matrix = build_similarity_matrix(mood_filtered_df)

    # Get song recommendations (ensuring 100 recommendations)
    recommendations = recommend_songs(mood_filtered_df, song_index, similarity_matrix, num_recommendations=20)

    # Display recommended songs
    print("\nRecommended Songs:")
    for song in recommendations:
        print(song)

if __name__ == "__main__":
    main()
