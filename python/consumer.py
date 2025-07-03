import json
from kafka import KafkaConsumer
import psycopg2
from datetime import datetime

consumer = KafkaConsumer(
    'user_activity',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True
)

conn = psycopg2.connect(
    dbname='events',
    user='postgres',
    password='postgres',
    host='postgres'
)
cursor = conn.cursor()
print("before read from kafka")
for msg in consumer:
    event = msg.value
    print(event)
    user_id = event['user_id']
    timestamp = datetime.fromisoformat(event['timestamp'])
    event_type = event['event_type']
    event_hour = timestamp.replace(minute=0, second=0, microsecond=0)
    event_minute = timestamp.replace(second=0, microsecond=0)
    

    cursor.execute("""
        INSERT INTO user_event_summary (user_id, event_hour,event_minute, event_type, event_count)
        VALUES (%s, %s, %s, %s, 1)
        ON CONFLICT (user_id, event_minute, event_type)
        DO UPDATE SET event_count = user_event_summary.event_count + 1
    """, (user_id, event_minute, event_minute, event_type))
    conn.commit()
    print(f"[{datetime.utcnow().isoformat()}] Processed:", event)
