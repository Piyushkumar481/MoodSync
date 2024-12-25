from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def build_similarity_matrix(df):
    """
    Builds a cosine similarity matrix based on the features in the dataframe.
    """
    # Use 'Genre_encoded' and 'User-Rating_normalized' for feature matrix
    feature_matrix = df[['Genre_encoded', 'User-Rating_normalized']].values
    
    # Compute cosine similarity
    similarity_matrix = cosine_similarity(feature_matrix)
    
    return similarity_matrix

def recommend_songs(df, song_index, similarity_matrix, num_recommendations=20):
    """
    Recommends songs based on cosine similarity.
    """
    # Get similarity scores for the given song
    similarity_scores = similarity_matrix[song_index]
    
    # Get indices of songs sorted by similarity (excluding the song itself)
    similar_songs = np.argsort(similarity_scores)[::-1]
    
    # Exclude the song itself (index 0)
    similar_songs = similar_songs[similar_songs != song_index]
    
    # Ensure that we have at least 100 recommendations
    recommended_songs = similar_songs[:max(num_recommendations, len(similar_songs))]
    
    # Return song names of the recommended songs
    return df.iloc[recommended_songs]['Song-Name'].values
