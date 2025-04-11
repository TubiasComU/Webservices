from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Microservices URLs
ORDERS_URL = "http://localhost:5001/orders"
KITCHEN_URL = "http://localhost:5002/kitchen"
PAYMENTS_URL = "http://localhost:5003/payments"

@app.route('/')
def home():
    return "API Gateway para Gestão de Restaurante!"

# Rout to create an order (POST for microservice Orders)
@app.route('/orders', methods=['POST'])
def create_order():
    order_data = request.json
    response = requests.post(ORDERS_URL, json=order_data)
    if response.status_code == 201:
        return jsonify(response.json()), 201
    return jsonify({"error": "Failed to create order"}), 400

# Route to send order to kitchen (POST for microservice Kitchen)
@app.route('/kitchen', methods=['POST'])
def send_to_kitchen():
    kitchen_data = request.json
    response = requests.post(KITCHEN_URL, json=kitchen_data)
    if response.status_code == 200:
        return jsonify({"message": "Order sent to kitchen!"}), 200
    return jsonify({"error": "Failed to send to kitchen"}), 400

# Route to process the payment (POST for microservice Payments)
@app.route('/payments', methods=['POST'])
def process_payment():
    payment_data = request.json
    response = requests.post(PAYMENTS_URL, json=payment_data)
    if response.status_code == 200:
        return jsonify({"message": "Payment processed successfully!"}), 200
    return jsonify({"error": "Payment processing failed"}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Porta 5000 para o Gateway
