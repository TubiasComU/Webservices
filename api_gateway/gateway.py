from flask import Flask, jsonify, request
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Microservices URLs
ORDERS_URL = "http://localhost:5001/orders"
KITCHEN_URL = "http://localhost:5002/kitchen"
PAYMENTS_URL = "http://localhost:5003/payments"

@app.route('/')
def home():
    return "API Gateway for a Restaurant"

# Route to create an order (POST for microservice Orders)
@app.route('/orders', methods=['POST' , 'GET'])
def create_order():
    order_data = request.json
    response = requests.post(ORDERS_URL, json=order_data)
    
    if response.status_code == 201:
        order_response_data = response.json()
        kitchen_response = requests.post(KITCHEN_URL, json=order_response_data)
        if kitchen_response.status_code == 200:
            return jsonify({
            "message": "Order created and sent to kitchen",
            "order": order_response_data
        }), 200

    
    return jsonify({"error": "Failed to create order"}), 400

# Route to send order to kitchen (POST for microservice Kitchen)
@app.route('/kitchen', methods=['POST' , 'GET'])
def send_to_kitchen():
    kitchen_data = request.json
    response = requests.post(KITCHEN_URL, json=kitchen_data)
    if response.status_code == 200:
        return jsonify({"message": "Order sent to kitchen!"}), 200
    return jsonify({"error": "Failed to send to kitchen"}), 400

# Route to process the payment (POST for microservice Payments)
@app.route('/payments', methods=['POST' , 'GET'])
def process_payment():
    payment_data = request.json
    response = requests.post(PAYMENTS_URL, json=payment_data)
    if response.status_code == 200:
        order_id = payment_data.get("order_id")

        # Update order status to paid
        update_url = f"{ORDERS_URL}/{order_id}"
        update_response = requests.patch(update_url, json={"status": "paid"})

        if update_response.status_code == 200:
            return jsonify({
                "message": "Payment processed and order marked as paid!"
            }), 200
        else:
            return jsonify({
                "message": "Payment processed, but failed to update order status."
            }), 207  # Multi-Status (207) indicates partial success

    return jsonify({"error": "Payment processing failed"}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Port for the API Gateway
