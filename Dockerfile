# Start with the official Python image.
FROM python:3.8-slim

# Set the working directory in the container.
WORKDIR /app

# Copy the requirements file to the container and install dependencies.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container.
COPY . .

# Set environment variables (adjust as needed).
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000
ENV KAFKA_BOOTSTRAP_SERVERS=localhost:9092 

# Expose the port that Flask will run on.
EXPOSE 5000

# Run the Flask app.
CMD ["flask", "run"]
