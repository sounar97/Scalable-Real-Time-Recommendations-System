from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import logging
from recommendation_engine import get_movie_recommendations, get_music_recommendations
from kafka_producer import send_user_interaction  # Import Kafka producer
from kafka_consumer import consume_interactions  # Import Kafka consumer
import threading

# Initialize Flask application
app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Set up logging
logging.basicConfig(level=logging.INFO)

# Load preprocessed movie and music data and similarity matrices
try:
    with open('Training/movies_list.pkl', 'rb') as file:
        movie_df = pickle.load(file)

    with open('Data/similarity.pkl', 'rb') as file:
        movie_similarity = pickle.load(file)

    with open('Training/df.pkl', 'rb') as file:
        music_df = pickle.load(file)

    with open('Data/similarity02.pkl', 'rb') as file:
        music_similarity = pickle.load(file)

except Exception as e:
    logging.error(f"Error loading data: {str(e)}")
    raise

# Start the real-time recommendations in a separate thread or as a background task
def start_real_time_recommendations():
    while True:
        user_interaction = consume_interactions()  # Get real-time interaction from Kafka
        if user_interaction:
            recommendations = get_movie_recommendations(user_interaction['title'], movie_df, movie_similarity)
            logging.info(f"Real-time recommendation for {user_interaction['title']}: {recommendations}")

# Run the real-time recommendation engine in a separate thread
threading.Thread(target=start_real_time_recommendations, daemon=True).start()

# Route to track and send user interactions to Kafka
@app.route('/api/track_interaction', methods=['POST'])
def track_interaction():
    data = request.get_json()
    interaction = data.get('interaction')
    
    if not interaction:
        return jsonify({'status': 'error', 'message': 'No interaction data provided'}), 400

    # Send the interaction to Kafka
    send_user_interaction({'interaction': interaction})
    
    return jsonify({'status': 'success', 'message': 'Interaction sent to Kafka'}), 200

# Movie recommendation route
@app.route('/recommend/movie', methods=['GET'])
def recommend_movie():
    title = request.args.get('title')
    if not title:
        return jsonify({'status': 'error', 'message': 'Title parameter is required'}), 400

    try:
        recommendations = get_movie_recommendations(title, movie_df, movie_similarity)
        return jsonify({'status': 'success', 'recommendations': recommendations})
    except Exception as e:
        logging.error(f"Error getting movie recommendations: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Music recommendation route
@app.route('/recommend/music', methods=['GET'])
def recommend_music():
    artist = request.args.get('artist')
    song = request.args.get('song')
    
    if not artist or not song:
        return jsonify({'status': 'error', 'message': 'Artist and song parameters are required'}), 400

    try:
        recommendations = get_music_recommendations(artist, song, music_df, music_similarity)
        return jsonify({'status': 'success', 'recommendations': recommendations})
    except Exception as e:
        logging.error(f"Error getting music recommendations: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
