# Scalable Real-Time Recommendations System

This project is a scalable recommendation system inspired by platforms like Netflix and Amazon. It provides real-time recommendations for movies and music based on user interactions. Built with Apache Kafka for data streaming, it enables efficient ingestion and processing of user data, making it suitable for dynamic environments where recommendations need to be updated frequently.

## Features

- **Real-Time Data Processing**: Uses Kafka for handling real-time interactions, ensuring data is processed immediately as it’s generated.
- **Scalable Architecture**: Deployed with Kubernetes to scale services based on demand.
- **Recommendation Engine**: Offers personalized recommendations for movies and music based on user interactions.
- **API Interface**: Exposes endpoints for interacting with the recommendation system.

## Tech Stack

- **Apache Kafka**: For real-time data streaming.
- **Kubernetes**: For deployment and scaling.
- **Docker**: For containerization of services.
- **Python**: For backend development with Flask.
- **Flask**: As the web framework for handling API requests.

## Repository Structure

```
Scalable-Real-Time-Recommendations-System/
├── Training/                   # Contains data and notebooks for preprocessing
├── kubernetes/                 # Kubernetes YAML files for deployment
│   ├── kafka-deployment.yaml
│   ├── kafka-service.yaml
│   ├── recommendation-service-deployment.yaml
│   ├── recommendation-service.yaml
│   ├── zookeeper-deployment.yaml
│   └── zookeeper-service.yaml
├── app.py                      # Main Flask app
├── kafka_consumer.py           # Kafka consumer code
├── kafka_producer.py           # Kafka producer code
├── recommendation_engine.py     # Recommendation logic for movies and music
├── config.py                   # Configuration file for topics and Kafka settings
├── Dockerfile                  # Dockerfile for building the application image
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```

## Prerequisites

1. **Docker** and **Docker Compose**
2. **Kubernetes** (Minikube or any other Kubernetes environment)
3. **kubectl** command-line tool for Kubernetes
4. **Kafka CLI** (if testing Kafka independently)
5. **Python 3.8+**

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/sounar97/Scalable-Real-Time-Recommendations-System.git
cd Scalable-Real-Time-Recommendations-System
```

### 2. Build the Docker Image

```bash
docker build -t recommendation-system .
```

### 3. Deploy to Kubernetes

The following steps assume a Kubernetes environment (local or cloud):

1. **Start Zookeeper**:

   ```bash
   kubectl apply -f kubernetes/zookeeper-deployment.yaml
   kubectl apply -f kubernetes/zookeeper-service.yaml
   ```

2. **Start Kafka**:

   ```bash
   kubectl apply -f kubernetes/kafka-deployment.yaml
   kubectl apply -f kubernetes/kafka-service.yaml
   ```

3. **Deploy the Recommendation Service**:

   ```bash
   kubectl apply -f kubernetes/recommendation-service-deployment.yaml
   kubectl apply -f kubernetes/recommendation-service.yaml
   ```

### 4. Access the Application

After deploying, you can access the recommendation service. If testing locally, you may port-forward the service:

```bash
kubectl port-forward service/recommendation-service 5000:5000
```

## API Endpoints

### 1. Recommend Movie

- **Endpoint**: `POST /api/v1/movies/recommend`
- **Description**: Generates movie recommendations based on a movie title.

#### Request Body

```json
{
  "title": "Joker"
}
```

#### Example cURL

```bash
curl -X POST http://localhost:5000/api/v1/movies/recommend -H "Content-Type: application/json" -d '{"title": "Joker"}'
```

### 2. Get Movie Results

- **Endpoint**: `GET /api/v1/movies/results/<session_id>`
- **Description**: Retrieves movie recommendations for a given session ID.

#### Example

```bash
curl -X GET http://localhost:5000/api/v1/movies/results/1731009967.5144303
```

### 3. Recommend Music

- **Endpoint**: `POST /api/v1/music/recommend`
- **Description**: Generates music recommendations based on a song title.
  
#### Request Body

```json
{
  "song": "Opportunities"
}
```

#### Example cURL

```bash
curl -X POST http://localhost:5000/api/v1/music/recommend -H "Content-Type: application/json" -d '{"song": "Opportunities"}'
```

### 4. Get Music Results

- **Endpoint**: `GET /api/v1/music/results/<session_id>`
- **Description**: Retrieves music recommendations for a given session ID.

#### Example

```bash
curl -X GET http://localhost:5000/api/v1/music/results/1731007938.9368248
```

### 5. Track User Interaction

- **Endpoint**: `POST /api/v1/track_interaction`
- **Description**: Records user interaction data for training or analytics purposes.

#### Request Body

```json
{
  "request_id": "1731009967.5144303",
  "interaction_type": "movie_recommendation_request",
}
```


## Running Locally with Docker Compose (Alternative to Kubernetes)

For simpler local testing, you can use Docker Compose to bring up Zookeeper, Kafka, and the recommendation service.

```bash
docker-compose up --build
```

## Testing the Setup

After the setup, test the endpoints using the example API requests provided above. You can use tools like **Postman** or **curl** to make API requests and validate responses.

## Scaling the Service

In Kubernetes, you can scale the recommendation service by updating the `replicas` field in `recommendation-service-deployment.yaml`. For example:

```yaml
spec:
  replicas: 3  # Scale up or down based on requirements
```

Then, apply the update:

```bash
kubectl apply -f kubernetes/recommendation-service-deployment.yaml
```

## Logging and Monitoring

To view logs of any pod, use:

```bash
kubectl logs -f <pod-name>
```

Replace `<pod-name>` with the name of the specific pod you wish to monitor.

## Contributing

If you'd like to contribute, please fork the repository and make a pull request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License.


