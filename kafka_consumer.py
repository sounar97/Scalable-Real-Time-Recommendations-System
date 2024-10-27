from confluent_kafka import Consumer, KafkaException

# Basic configuration for Kafka consumer
consumer_config = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'my-group',  # Consumer group ID for Kafka
    'auto.offset.reset': 'earliest'  # Start reading from the beginning
}

# Create a Kafka consumer
consumer = Consumer(consumer_config)

# Subscribe to the user interactions topic
consumer.subscribe(['user_interactions'])

def consume_interactions():
    """
    Consume user interaction messages from Kafka.
    """
    try:
        # Poll for new messages with the specified timeout
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            return None
        if msg.error():
            raise KafkaException(msg.error())
        
        # Deserialize the message back into a Python object
        interaction = msg.value().decode('utf-8')
        return interaction
    
    except Exception as e:
        print(f"Error in Kafka consumer: {e}")
        return None

# Example usage of the consumer function
while True:
    interaction = consume_interactions()
    if interaction:
        print("Consumed interaction:", interaction)
