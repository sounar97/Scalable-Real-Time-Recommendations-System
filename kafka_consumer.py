from confluent_kafka import Consumer, KafkaException

# Configuration for Kafka consumer with custom fetch size and max poll records
consumer_config = {
    'bootstrap.servers': 'localhost:9092',  
    'group.id': 'recommendation_group',
    'auto.offset.reset': 'earliest',
    'fetch.min.bytes': 1024,  # Fetch at least 1 KB of messages before returning
    'max.poll.records': 500  # Fetch a maximum of 500 messages per poll to balance performance
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
        interaction = eval(msg.value().decode('utf-8'))  # Adjust based on serialization format
        return interaction
    
    except Exception as e:
        print(f"Error in Kafka consumer: {e}")
        return None

# Example usage of the consumer function
interaction = consume_interactions()
if interaction:
    print("Consumed interaction:", interaction)
