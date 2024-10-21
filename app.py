from flask import Flask, request, jsonify
import pickle
from recommendation_engine import get_movie_recommendations, get_music_recommendations

app = Flask(__name__)

# Load preprocessed movie and music data and similarity matrices
with open('Training/movies_list.pkl', 'rb') as file:
    movie_df = pickle.load(file)

with open('Data/similarity.pkl', 'rb') as file:
    movie_similarity = pickle.load(file)

with open('Training/df.pkl', 'rb') as file:
    music_df = pickle.load(file)

with open('Data/similarity02.pkl', 'rb') as file:
    music_similarity = pickle.load(file)

@app.route('/recommend/movie', methods=['GET'])
def recommend_movie():
    title = request.args.get('title')
    try:
        recommendations = get_movie_recommendations(title, movie_df, movie_similarity)
        return jsonify({'status': 'success', 'recommendations': recommendations})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/recommend/music', methods=['GET'])
def recommend_music():
    artist = request.args.get('artist')
    song = request.args.get('song')
    try:
        recommendations = get_music_recommendations(artist, song, music_df, music_similarity)
        return jsonify({'status': 'success', 'recommendations': recommendations})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
