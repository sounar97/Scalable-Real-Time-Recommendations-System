from confluent_kafka import Consumer, KafkaException

# Configuration for Kafka consumer
consumer_config = {
    'bootstrap.servers': 'localhost:9092',  
    'group.id': 'recommendation_group',
    'auto.offset.reset': 'earliest'
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
        msg = consumer.poll(timeout=1.0)  # Poll for new messages
        if msg is None:
            return None
        if msg.error():
            raise KafkaException(msg.error())
        # Deserialize the message back into a Python object
        interaction = eval(msg.value().decode('utf-8'))  # You may need to adjust this depending on how you serialize it
        return interaction
    except Exception as e:
        print(f"Error in Kafka consumer: {e}")
        return None
