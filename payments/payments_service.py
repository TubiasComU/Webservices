from flask import Flask, request, jsonify
import json
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

PAYMENTS_FILE = 'payments/payments.json'
payments = []

# Load payments from JSON file
def load_payments():
    global payments
    if os.path.exists(PAYMENTS_FILE):
        with open(PAYMENTS_FILE, 'r') as f:
            payments = json.load(f)

# Save payments to JSON file
def save_payments():
    with open(PAYMENTS_FILE, 'w') as f:
        json.dump(payments, f, indent=2)

@app.route('/payments', methods=['POST'])
def process_payment():
    data = request.json
    id = data.get('id')
    amount = data.get('amount')

    if not id or not amount:
        return jsonify({'error': 'Missing id or amount'}), 400

    payment = {
        'id': id,
        'amount': amount,
        'status': 'paid'
    }
    payments.append(payment)
    save_payments()
    return jsonify({'message': 'Payment successful'}), 200

@app.route('/payments', methods=['GET'])
def get_payments():
    return jsonify(payments), 200

if __name__ == '__main__':
    load_payments()
    app.run(debug=True, port=5003)
