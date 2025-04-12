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

    if 'table' in data:
        table_number = data['table']
        
        # Verifies if the table number already exists in the payments list
        if any(p.get('table') == table_number for p in payments):
            return jsonify({'message': f'Payment entry for table {table_number} already exists'}), 200

        payment = {
            'table': table_number,
            'paid': 0  # Default to unpaid
        }
        payments.append(payment)
        save_payments()
        return jsonify({'message': 'Payment entry created'}), 200

    return jsonify({'error': 'Missing table field'}), 400

@app.route('/payments', methods=['GET'])
def get_payments():
    return jsonify(payments), 200

@app.route('/payments/<int:table>', methods=['PATCH'])
def update_payment(table):
    data = request.json
    for payment in payments:
        if payment["table"] == table:
            payment["paid"] = data.get("paid", payment["paid"])
            save_payments()
            return jsonify(payment), 200
    return jsonify({"error": "Payment not found"}), 404

if __name__ == '__main__':
    load_payments()
    app.run(debug=True, port=5003)
