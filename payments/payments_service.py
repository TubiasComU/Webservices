from flask import Flask, request, jsonify
import json
import os
from flask_cors import CORS
import requests
import threading
import time

ORDERS_URL = "http://localhost:5001/orders"
KITCHEN_URL = "http://localhost:5002/kitchen"

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
        
        # Verifica se já existe entrada para a mesa
        if any(p.get('table') == table_number for p in payments):
            return jsonify({'message': f'Payment entry for table {table_number} already exists'}), 200

        payment = {
            'table': table_number,
            'paid': 0
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

            if payment["paid"] == 1:
                # Remove from orders and kitchen microservices
                try:
                    requests.delete(f"{ORDERS_URL}/table/{table}")
                    requests.delete(f"{KITCHEN_URL}/table/{table}")
                except requests.exceptions.RequestException as e:
                    print("❌ Error deleting orders/kitchen:", e)

                # Iniciate a thread to remove the payment after 20 seconds
                threading.Thread(target=remove_payment_after_delay, args=(table,), daemon=True).start()

            return jsonify(payment), 200

    return jsonify({"error": "Payment not found"}), 404

# Remove the payment entry after 20 seconds
def remove_payment_after_delay(table):
    time.sleep(20)
    global payments
    payments = [p for p in payments if p["table"] != table]
    save_payments()
    print(f"✅ Payment for table {table} removed after 20 seconds")

if __name__ == '__main__':
    load_payments()
    app.run(debug=True, port=5003)
