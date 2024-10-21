import pandas as pd

# Movie recommendation function
def get_movie_recommendations(title, df, similarity_matrix):
    # Check if the title exists in the dataset
    if title not in df['title'].values:
        raise ValueError(f"Title '{title}' not found in dataset.")

    # Get the index of the movie
    index = df[df['title'] == title].index[0]

    # Compute similarity scores
    similarity_scores = list(enumerate(similarity_matrix[index]))

    # Sort scores based on similarity, excluding the first (which is the same movie)
    sorted_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

    # Get top 5 recommendations (excluding the movie itself)
    recommended_titles = [df['title'].iloc[i[0]] for i in sorted_scores[1:6]]

    return recommended_titles

# Music recommendation function
def get_music_recommendations(artist, song_title, df, similarity_matrix):
    # Check if the artist and song exist in the dataset
    song_exists = df[(df['artist'] == artist) & (df['song'] == song_title)]
    if song_exists.empty:
        raise ValueError(f"Song '{song_title}' by artist '{artist}' not found in dataset.")

    # Get the index of the song
    index = song_exists.index[0]

    # Compute similarity scores
    similarity_scores = list(enumerate(similarity_matrix[index]))

    # Sort scores based on similarity, excluding the first (which is the same song)
    sorted_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

    # Get top 5 recommendations (excluding the song itself)
    recommended_songs = [df['song'].iloc[i[0]] for i in sorted_scores[1:6]]

    return recommended_songs
