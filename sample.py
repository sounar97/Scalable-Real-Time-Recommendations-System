from flask import Flask, request, jsonify
from kafka import KafkaProducer, KafkaConsumer
import pickle
import json
import threading
import time
import logging
import os

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Kafka Configuration
KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'
MOVIE_REQUEST_TOPIC = 'movie_recommendation_requests'
MUSIC_REQUEST_TOPIC = 'music_recommendation_requests'
MOVIE_RESPONSE_TOPIC = 'movie_recommendation_responses'
MUSIC_RESPONSE_TOPIC = 'music_recommendation_responses'

# Load recommendation models
try:
    movies_df = pickle.load(open('movies_list.pkl', 'rb'))
    movies_similarity = pickle.load(open('similarity.pkl', 'rb'))
    music_df = pickle.load(open('df.pkl', 'rb'))
    music_similarity = pickle.load(open('similarity02.pkl', 'rb'))
    logger.info("Models loaded successfully")
except Exception as e:
    logger.error(f"Error loading models: {str(e)}")
    raise

def create_kafka_producer():
    """Create and return a Kafka producer instance"""
    try:
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        return producer
    except Exception as e:
        logger.error(f"Error creating Kafka producer: {str(e)}")
        raise

def create_kafka_consumer(topic):
    """Create and return a Kafka consumer instance"""
    try:
        consumer = KafkaConsumer(
            topic,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            auto_offset_reset='latest',
            enable_auto_commit=True
        )
        return consumer
    except Exception as e:
        logger.error(f"Error creating Kafka consumer: {str(e)}")
        raise

# Create Kafka producer
producer = create_kafka_producer()

def get_movie_recommendations(title, request_id):
    """Generate movie recommendations"""
    try:
        idx = movies_df[movies_df['title'] == title].index[0]
        distances = sorted(list(enumerate(movies_similarity[idx])), reverse=True, key=lambda x: x[1])
        recommendations = []
        
        for i in distances[1:6]:  # Get top 5 recommendations
            movie_data = movies_df.iloc[i[0]]
            recommendations.append({
                'title': movie_data['title'],
                'genre': movie_data['genre'],
                'similarity_score': float(i[1])
            })
        
        return {
            'request_id': request_id,
            'status': 'success',
            'recommendations': recommendations
        }
    except Exception as e:
        return {
            'request_id': request_id,
            'status': 'error',
            'error': str(e)
        }

def get_music_recommendations(title, request_id):
    """Generate music recommendations"""
    try:
        idx = music_df[music_df['song'] == title].index[0]
        distances = sorted(list(enumerate(music_similarity[idx])), reverse=True, key=lambda x: x[1])
        recommendations = []
        
        for i in distances[1:6]:  # Get top 5 recommendations
            song_data = music_df.iloc[i[0]]
            recommendations.append({
                'song': song_data['song'],
                'artist': song_data['artist'],
                'similarity_score': float(i[1])
            })
        
        return {
            'request_id': request_id,
            'status': 'success',
            'recommendations': recommendations
        }
    except Exception as e:
        return {
            'request_id': request_id,
            'status': 'error',
            'error': str(e)
        }

# Kafka consumer threads
def movie_consumer_thread():
    """Thread to handle movie recommendation requests"""
    consumer = create_kafka_consumer(MOVIE_REQUEST_TOPIC)
    for message in consumer:
        data = message.value
        response = get_movie_recommendations(data['title'], data['request_id'])
        producer.send(MOVIE_RESPONSE_TOPIC, response)
        producer.flush()

def music_consumer_thread():
    """Thread to handle music recommendation requests"""
    consumer = create_kafka_consumer(MUSIC_REQUEST_TOPIC)
    for message in consumer:
        data = message.value
        response = get_music_recommendations(data['song'], data['request_id'])
        producer.send(MUSIC_RESPONSE_TOPIC, response)
        producer.flush()

# Start consumer threads
threading.Thread(target=movie_consumer_thread, daemon=True).start()
threading.Thread(target=music_consumer_thread, daemon=True).start()

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
        
        # Send request to Kafka
        producer.send(MOVIE_REQUEST_TOPIC, message)
        producer.flush()
        
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
        
        # Send request to Kafka
        producer.send(MUSIC_REQUEST_TOPIC, message)
        producer.flush()
        
        return jsonify({
            'request_id': request_id,
            'message': 'Request received, processing recommendations'
        })
    
    except Exception as e:
        logger.error(f"Error in music recommendations: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)