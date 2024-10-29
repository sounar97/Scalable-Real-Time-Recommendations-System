# kafka_producer.py
from kafka import KafkaProducer
import json
import logging
from config import KAFKA_BOOTSTRAP_SERVERS

logger = logging.getLogger(__name__)

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