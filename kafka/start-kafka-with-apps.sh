#!/bin/bash

# Start Kafka in the background#!/bin/bash

# Start Kafka in the background
/opt/bitnami/scripts/kafka/entrypoint.sh /opt/bitnami/scripts/kafka/run.sh &

echo "⏳ Waiting for Kafka to start..."
until nc -z localhost 9092; do sleep 1; done
# Wait for PostgreSQL
echo "⏳ Waiting for PostgreSQL..."
until nc -z postgres 5432; do sleep 1; done

# Create Kafka topic
echo "✅ Creating Kafka topic: user_activity"
/opt/bitnami/kafka/bin/kafka-topics.sh \
  --create \
  --topic user_activity \
  --bootstrap-server localhost:9092 \
  --partitions 1 \
  --replication-factor 1 \
  --if-not-exists

# Run producer and consumer
echo "🚀 Starting producer and consumer apps..."
python3 /python-app/producer.py &
python3 /python-app/consumer.py &

# Keep container alive
tail -f /dev/null
