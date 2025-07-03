import time
import json
import random
from kafka import KafkaProducer
from datetime import datetime

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

event_types = ['click', 'view', 'scroll']

while True:
    event = {
        'user_id': f"user_{random.randint(1, 5)}",
        'timestamp': datetime.utcnow().isoformat(),
        'event_type': random.choice(event_types)
    }
    print(event)
    producer.send('user_activity', value=event)
    print(f"[{datetime.utcnow().isoformat()}] Produced:", event)
    time.sleep(random.uniform(0.5, 2))
