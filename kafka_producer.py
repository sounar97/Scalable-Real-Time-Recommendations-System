# kafka_producer.py
from kafka import KafkaProducer
import json
import logging
from config import KAFKA_BOOTSTRAP_SERVERS
from config import USER_INTERACTION_TOPIC

logger = logging.getLogger(__name__)

def create_kafka_producer():
    """Create and return Kafka producer instances"""
    try:
        rec_producer = KafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

        int_producer = KafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

        return rec_producer, int_producer
    except Exception as e:
        logger.error(f"Error creating Kafka producers: {str(e)}")
        raise
    
def send_interaction_to_kafka(interaction_data, producer):
    """Send user interaction data to Kafka"""
    # No additional encoding needed, as the producer already uses `json.dumps`
    producer.send(USER_INTERACTION_TOPIC, interaction_data)
    producer.flush()
