from confluent_kafka import Producer

# Configuration for Kafka producer
producer_config = {
    'bootstrap.servers': 'localhost:9092'  # Adjust as per your Kafka setup
}

# Create a Kafka producer
producer = Producer(producer_config)

def send_user_interaction(interaction_data):
    """
    Send user interaction to Kafka.
    """
    topic = 'user_interactions'
    
    # Convert interaction data to a string (or JSON format)
    message = str(interaction_data)
    
    # Send the message to Kafka topic
    producer.produce(topic, message)
    producer.flush()
