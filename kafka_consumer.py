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
    MUSIC_RESPONSE_TOPIC,
    USER_INTERACTION_TOPIC
)
from recommendation_engine import get_movie_recommendations, get_music_recommendations
from kafka_producer import create_kafka_producer

logger = logging.getLogger(__name__)
producer = create_kafka_producer()

# In-memory storage for results
movie_results = defaultdict(dict)
music_results = defaultdict(dict)
user_interactions = defaultdict(list)

def create_kafka_consumer(topic):
    """Create and return a Kafka consumer instance"""
    try:
        consumer = KafkaConsumer(
            topic,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            auto_offset_reset='latest',
            group_id='recommendation_group',  # Add a consumer group
            enable_auto_commit=True
        )
        return consumer
    except Exception as e:
        logger.error(f"Error creating Kafka consumer: {str(e)}")
        raise

def movie_consumer_thread():
    """Thread to handle movie recommendation requests"""
    while True:  # Add infinite loop
        try:
            consumer = create_kafka_consumer(MOVIE_REQUEST_TOPIC)
            for message in consumer:
                try:
                    data = message.value
                    logger.info(f"Received movie request: {data}")
                    response = get_movie_recommendations(data['title'], data['request_id'], {})
                    movie_results[data['request_id']] = response
                    producer.send(MOVIE_RESPONSE_TOPIC, response)
                    producer.flush()
                    logger.info(f"Processed movie request: {data['request_id']}")
                except Exception as e:
                    logger.error(f"Error processing movie message: {str(e)}")
        except Exception as e:
            logger.error(f"Error in movie consumer thread: {str(e)}")
            continue

def music_consumer_thread():
    """Thread to handle music recommendation requests"""
    while True:  # Add infinite loop
        try:
            consumer = create_kafka_consumer(MUSIC_REQUEST_TOPIC)
            for message in consumer:
                try:
                    data = message.value
                    logger.info(f"Received music request: {data}")
                    response = get_music_recommendations(data['song'], data['request_id'], {})
                    music_results[data['request_id']] = response
                    producer.send(MUSIC_RESPONSE_TOPIC, response)
                    producer.flush()
                    logger.info(f"Processed music request: {data['request_id']}")
                except Exception as e:
                    logger.error(f"Error processing music message: {str(e)}")
        except Exception as e:
            logger.error(f"Error in music consumer thread: {str(e)}")
            continue

def user_interaction_consumer_thread():
    """Thread to handle user interaction data"""
    while True:  # Add infinite loop
        try:
            consumer = create_kafka_consumer(USER_INTERACTION_TOPIC)
            for message in consumer:
                try:
                    data = message.value
                    logger.info(f"Received user interaction: {data}")
                    user_interactions[data['request_id']].append(data)
                except Exception as e:
                    logger.error(f"Error processing interaction message: {str(e)}")
        except Exception as e:
            logger.error(f"Error in user interaction consumer thread: {str(e)}")
            continue

def start_consumer_threads():
    """Start all consumer threads"""
    threads = [
        threading.Thread(target=movie_consumer_thread, daemon=True),
        threading.Thread(target=music_consumer_thread, daemon=True),
        threading.Thread(target=user_interaction_consumer_thread, daemon=True)
    ]
    
    for thread in threads:
        thread.start()
    
    logger.info("All consumer threads started")