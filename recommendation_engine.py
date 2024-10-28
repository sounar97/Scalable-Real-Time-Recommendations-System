import pandas as pd
from kafka_consumer import consume_interactions  # Ensure this module exists

# Movie recommendation function
def get_movie_recommendations(title, movie_df, similarity_matrix, top_n=5):
    """
    Generate top movie recommendations based on similarity scores.
    """
    if title not in movie_df['title'].values:
        raise ValueError(f"Title '{title}' not found in dataset.")

    # Get index and similarity scores
    index = movie_df[movie_df['title'] == title].index[0]
    similarity_scores = list(enumerate(similarity_matrix[index]))

    # Sort and get top N recommendations
    sorted_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    recommended_titles = [movie_df['title'].iloc[i[0]] for i in sorted_scores[1:top_n + 1]]

    return recommended_titles

# Music recommendation function
def get_music_recommendations(artist, song_title, music_df, similarity_matrix, top_n=5):
    """
    Generate top music recommendations based on similarity scores.
    """
    song_exists = music_df[(music_df['artist'] == artist) & (music_df['song'] == song_title)]
    if song_exists.empty:
        raise ValueError(f"Song '{song_title}' by artist '{artist}' not found in dataset.")

    # Get index and similarity scores
    index = song_exists.index[0]
    similarity_scores = list(enumerate(similarity_matrix[index]))

    # Sort and get top N recommendations
    sorted_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    recommended_songs = [music_df['song'].iloc[i[0]] for i in sorted_scores[1:top_n + 1]]

    return recommended_songs

# Real-time recommendation engine
def real_time_recommendations(movie_df, movie_similarity_matrix, music_df, music_similarity_matrix):
    """
    Continuously listen for user interactions and provide recommendations.
    """
    while True:
        user_interaction = consume_interactions()  # Get real-time interaction

        movie_title = user_interaction.get('movie_title')
        artist = user_interaction.get('artist')
        song_title = user_interaction.get('song_title')

        recommendations = []

        # Generate movie recommendations if movie title is provided
        if movie_title:
            try:
                movie_recommendations = get_movie_recommendations(movie_title, movie_df, movie_similarity_matrix)
                recommendations.append({"type": "movie", "recommendations": movie_recommendations})
            except ValueError as e:
                print(f"Movie recommendation error: {e}")

        # Generate music recommendations if artist and song title are provided
        if artist and song_title:
            try:
                music_recommendations = get_music_recommendations(artist, song_title, music_df, music_similarity_matrix)
                recommendations.append({"type": "music", "recommendations": music_recommendations})
            except ValueError as e:
                print(f"Music recommendation error: {e}")

        # Output or store recommendations
        if recommendations:
            print(recommendations)  # Replace with your storage solution if needed
