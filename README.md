<br> <h2>Transaction Streaming and Retrieval with Kafka, Aerospike, and Flask </h2> </br>
This repository demonstrates a simple data pipeline for generating transaction events, publishing them to Kafka, storing them in Aerospike, and providing a RESTful endpoint to retrieve specific transactions. This is a test version of a connection that I am familiar with. 

<h3>Overview</h3>
<h4>Components</h4>

 <ins> Kafka Producer and Aerospike Insertion (Producer Script): </ins>


Generates random transaction data.
Publishes the transaction events to a Kafka topic (transactions). </br>
Simultaneously inserts the same events into an Aerospike database for persistence. </br>


<ins> Flask Application for Retrieval (API Script): </ins>

Exposes a RESTful API endpoint to fetch a transaction based on card_id and timestamp. </br>
Connects to the Aerospike database to retrieve and return the transaction data as JSON. </br>


<h4> Workflow </h4>
The producer script generates synthetic transaction records, each containing: </br></br>

card_id</br>
amount</br>
location</br>
merchant</br>
timestamp</br>
</br>
Each record is: </br>

Sent to a Kafka topic named transactions.
Inserted into Aerospike for storage with a primary index of cardID+TimeStamp combination.</br></br>
The Flask application provides a retrieval endpoint:</br>

GET /fetch/<card_id>/<timestamp> returns the transaction record matching the given card_id and timestamp from Aerospike.
Prerequisites
Python 3.7+ installed.
Kafka and Zookeeper running locally.
Aerospike server running locally.
Kafka and Zookeeper Setup
You must have a running Kafka cluster. </br></br>



Running the Producer Script</br> 

The producer script:</br>

Connects to Kafka on localhost:9092.
Connects to Aerospike on 127.0.0.1:3000.
Generates 10 sample transactions and sends them to Kafka and Aerospike.

To run the script:</br></br>

python aerospike-kafka.py.py
You should see an output indicating that transactions are being sent to Kafka and inserted into Aerospike. </br></br>

Running the Flask Application</br>
The Flask app:</br>

Connects to Aerospike.</br>
Provides a GET /fetch/<card_id>/<timestamp> endpoint to retrieve transactions.</br>
To start the Flask server:</br>


python get_api.py
The application will run on http://localhost:5000.

Testing the Retrieval Endpoint</br>
After generating transactions, you can fetch a record by sending a GET request. For example, if you know the card_id and the exact timestamp of the transaction:</br></br>

curl http://localhost:5000/fetch/1603115/2024-12-08%2012:34:56.789012
If the record exists, you will receive a JSON response with the transaction details. If not found, you’ll get an error message.
