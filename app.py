# app.py
from flask import Flask, request, jsonify
import time
import logging
from kafka_producer import create_kafka_producer,send_interaction_to_kafka
from kafka_consumer import start_consumer_threads, movie_results, music_results
from config import MOVIE_REQUEST_TOPIC, MUSIC_REQUEST_TOPIC,USER_INTERACTION_TOPIC

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
producer = create_kafka_producer()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': time.time()})

@app.route('/api/v1/movies/recommend', methods=['POST'])
def movie_recommendations():
    """Endpoint for movie recommendations"""
    try:
        data = request.get_json()
        if not data or 'title' not in data:
            return jsonify({'error': 'Missing title in request'}), 400
        request_id = str(time.time())
        message = {
            'title': data['title'],
            'request_id': request_id
        }

        rec_producer, int_producer = create_kafka_producer()
        rec_producer.send(MOVIE_REQUEST_TOPIC, message)
        rec_producer.flush()

        # Capture user interaction data
        interaction_data = {
            'title': data['title'],
            'interaction_type': 'movie_recommendation_request'
        }
        int_producer.send(USER_INTERACTION_TOPIC, interaction_data)
        int_producer.flush()

        return jsonify({
            'request_id': request_id,
            'message': 'Request received, processing recommendations'
        })
    except Exception as e:
        logger.error(f"Error in movie recommendations: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/music/recommend', methods=['POST'])
def music_recommendations():
    """Endpoint for music recommendations"""
    try:
        data = request.get_json()
        if not data or 'song' not in data:
            return jsonify({'error': 'Missing song in request'}), 400
        request_id = str(time.time())
        message = {
            'song': data['song'],
            'request_id': request_id
        }

        rec_producer, int_producer = create_kafka_producer()
        rec_producer.send(MUSIC_REQUEST_TOPIC, message)
        rec_producer.flush()

        # Capture user interaction data
        interaction_data = {
            'song': data['song'],
            'interaction_type': 'music_recommendation_request'
        }
        int_producer.send(USER_INTERACTION_TOPIC, interaction_data)
        int_producer.flush()

        return jsonify({
            'request_id': request_id,
            'message': 'Request received, processing recommendations'
        })
    except Exception as e:
        logger.error(f"Error in music recommendations: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/movies/results/<request_id>', methods=['GET'])
def get_movie_results(request_id):
    """Get movie recommendation results"""
    result = movie_results.get(request_id)
    if result:
        return jsonify(result)
    else:
        return jsonify({'error': 'Results not found or still processing'}), 404

@app.route('/api/v1/music/results/<request_id>', methods=['GET'])
def get_music_results(request_id):
    """Get music recommendation results"""
    result = music_results.get(request_id)
    if result:
        return jsonify(result)
    else:
        return jsonify({'error': 'Results not found or still processing'}), 404

@app.route('/api/v1/track_interaction', methods=['POST'])
def track_interaction():
    try:
        data = request.get_json()
        if not data or 'request_id' not in data or 'interaction_type' not in data:
            return jsonify({'error': 'Missing required fields in request'}), 400

        producer = create_kafka_producer()
        send_interaction_to_kafka(data, producer)

        return jsonify({'status': 'success'})
    except Exception as e:
        logger.error(f"Error tracking interaction: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    start_consumer_threads()
    app.run(host='0.0.0.0', port=5000, debug=True)
    