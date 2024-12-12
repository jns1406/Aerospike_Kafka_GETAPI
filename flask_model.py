from flask import Flask, request, jsonify
import joblib
import aerospike

app = Flask(__name__)
model = joblib.load('fraud_model.pkl')

# Aerospike connection
config = {'hosts': [('127.0.0.1', 3000)]}
client = aerospike.client(config).connect()

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    features = [[data['amount'], data['location'], data['merchant']]]
    prediction = model.predict(features)
    
    response = {
        "fraud": bool(prediction[0]),
        "card_id": data['card_id']
    }

    # Store result in Aerospike
    key = ('test', 'fraud_results', data['card_id'])
    client.put(key, {**data, 'fraud': response['fraud']})

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
