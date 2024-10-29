from kafka import KafkaConsumer
import json
import threading
import logging
from collections import defaultdict
from config import (
    KAFKA_BOOTSTRAP_SERVERS, 
    MOVIE_REQUEST_TOPIC, 
    MUSIC_REQUEST_TOPIC,
    MOVIE_RESPONSE_TOPIC,
    MUSIC_RESPONSE_TOPIC
)
from recommendation_engine import get_movie_recommendations, get_music_recommendations
from kafka_producer import create_kafka_producer

logger = logging.getLogger(__name__)
producer = create_kafka_producer()

# In-memory storage for results
movie_results = defaultdict(dict)
music_results = defaultdict(dict)

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

def movie_consumer_thread():
    """Thread to handle movie recommendation requests"""
    consumer = create_kafka_consumer(MOVIE_REQUEST_TOPIC)
    for message in consumer:
        data = message.value
        response = get_movie_recommendations(data['title'], data['request_id'])
        movie_results[data['request_id']] = response  # Store results
        producer.send(MOVIE_RESPONSE_TOPIC, response)
        producer.flush()

def music_consumer_thread():
    """Thread to handle music recommendation requests"""
    consumer = create_kafka_consumer(MUSIC_REQUEST_TOPIC)
    for message in consumer:
        data = message.value
        response = get_music_recommendations(data['song'], data['request_id'])
        music_results[data['request_id']] = response  # Store results
        producer.send(MUSIC_RESPONSE_TOPIC, response)
        producer.flush()

def start_consumer_threads():
    """Start all consumer threads"""
    threading.Thread(target=movie_consumer_thread, daemon=True).start()
    threading.Thread(target=music_consumer_thread, daemon=True).start()