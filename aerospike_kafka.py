from kafka import KafkaProducer
import json
import time
import random
from datetime import datetime
import aerospike

# Initialize Kafka Producer
producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda x: json.dumps(x).encode('utf-8'))

# Aerospike client configuration
config = {'hosts': [('127.0.0.1', 3000)]}
client = aerospike.client(config).connect()


# insertion into aerospike db

def insert_into_aerospike(transaction):
    key = ('test', 'transactions', transaction['card_id'] + "_" + transaction['timestamp'])
    try:
        client.put(key, transaction)
        print(f"Inserted into Aerospike: {transaction}")
    except Exception as e:
        print(f"Error inserting into Aerospike: {e}")


# for kafka data streaming

def generate_transaction():
    card_ids = ["1603115", "1464161", "5555555"]
    locations = ["New York", "Los Angeles", "Chicago"]
    merchants = ["Online Store", "Grocery", "Gas Station"]
    
    record_count = 0
    max_records = 10

    while record_count < max_records:
        transaction = {
            "card_id": random.choice(card_ids),
            "amount": round(random.uniform(5, 500), 2),
            "location": random.choice(locations),
            "merchant": random.choice(merchants),
            "timestamp": str(datetime.now())
        }

        # Send transaction (topic)  to Kafka
        producer.send('transactions', value=transaction)
        print(f"Sent: {transaction}")

        # Insert transaction into Aerospike
        insert_into_aerospike(transaction)

        time.sleep(0.1)  # Short delay to control the rate
        record_count += 1

    print(f"Generated {max_records} transactions.")
    client.close()  # Close Aerospike connection

generate_transaction()
