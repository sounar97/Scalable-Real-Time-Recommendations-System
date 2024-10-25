from confluent_kafka import Producer

# Configuration for Kafka producer with batching, compression, and linger time
producer_config = {
    'bootstrap.servers': 'localhost:9092',  # Adjust to your Kafka setup
    'linger.ms': 10,  # Wait for 10ms to batch messages
    'batch.size': 65536,  # 64 KB batch size for more efficient delivery
    'compression.type': 'gzip'  # Compress messages to reduce size and network usage
}

# Create a Kafka producer
producer = Producer(producer_config)

def delivery_report(err, msg):
    """Callback function to handle delivery reports."""
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

def send_user_interaction(interaction_data):
    """
    Send user interaction to Kafka.
    """
    topic = 'user_interactions'
    
    # Convert interaction data to a string (or JSON format)
    message = str(interaction_data)
    
    # Send the message to Kafka topic
    # You can also specify a key if needed, e.g., key='user_id'
    producer.produce(topic, key=None, value=message, callback=delivery_report)
    producer.flush()  # Ensure all messages are sent before closing the producer

# Example usage:
interaction = {'user_id': 123, 'interaction_type': 'click', 'timestamp': '2024-10-25T12:34:56'}
send_user_interaction(interaction)
