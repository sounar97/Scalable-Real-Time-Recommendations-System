# recommendation_engine.py
import pickle
import logging
from config import (USER_INTERACTION_TOPIC,MOVIE_RESPONSE_TOPIC,
    MUSIC_RESPONSE_TOPIC)

logger = logging.getLogger(__name__)

# Load recommendation models
try:
    movies_df = pickle.load(open('Training\movies_list.pkl', 'rb'))
    movies_similarity = pickle.load(open('Data\similarity.pkl', 'rb'))
    music_df = pickle.load(open('Training\df.pkl', 'rb'))
    music_similarity = pickle.load(open('Data\similarity02.pkl', 'rb'))
    logger.info("Models loaded successfully")
except Exception as e:
    logger.error(f"Error loading models: {str(e)}")
    raise

from kafka_producer import create_kafka_producer

# Create Kafka producers
rec_producer, int_producer = create_kafka_producer()

def get_movie_recommendations(title, request_id, interaction_data):
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

        # Send the recommendation results to the Kafka producer
        response = {
            'request_id': request_id,
            'status': 'success',
            'recommendations': recommendations
        }
        rec_producer.send(MOVIE_RESPONSE_TOPIC, response)
        rec_producer.flush()

        # Send the interaction data to the Kafka producer
        interaction_data['request_id'] = request_id
        interaction_data['interaction_type'] = 'movie_recommendation'
        int_producer.send(USER_INTERACTION_TOPIC, interaction_data)
        int_producer.flush()

        return response
    except Exception as e:
        return {
            'request_id': request_id,
            'status': 'error',
            'error': str(e)
        }

def get_music_recommendations(song, request_id, interaction_data):
    """Generate music recommendations"""
    try:
        idx = music_df[music_df['song'] == song].index[0]
        distances = sorted(list(enumerate(music_similarity[idx])), reverse=True, key=lambda x: x[1])
        recommendations = []

        for i in distances[1:6]:  # Get top 5 recommendations
            song_data = music_df.iloc[i[0]]
            recommendations.append({
                'song': song_data['song'],
                'artist': song_data['artist'],
                'similarity_score': float(i[1])
            })

        # Send the recommendation results to the Kafka producer
        response = {
            'request_id': request_id,
            'status': 'success',
            'recommendations': recommendations
        }
        rec_producer.send(MUSIC_RESPONSE_TOPIC, response)
        rec_producer.flush()

        # Send the interaction data to the Kafka producer
        interaction_data['request_id'] = request_id
        interaction_data['interaction_type'] = 'music_recommendation'
        int_producer.send(USER_INTERACTION_TOPIC, interaction_data)
        int_producer.flush()

        return response
    except Exception as e:
        return {
            'request_id': request_id,
            'status': 'error',
            'error': str(e)
        }