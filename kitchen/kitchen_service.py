from flask import Flask, request, jsonify
import json
import os
import threading
import time
import random
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

KITCHEN_FILE = 'kitchen/kitchen_orders.json'
kitchen_queue = []

# Load orders from JSON file
def load_kitchen_orders():
    global kitchen_queue
    if os.path.exists(KITCHEN_FILE):
        with open(KITCHEN_FILE, 'r') as f:
            kitchen_queue = json.load(f)

# Save orders to JSON file
def save_kitchen_orders():
    with open(KITCHEN_FILE, 'w') as f:
        json.dump(kitchen_queue, f, indent=2)

@app.route('/kitchen', methods=['POST'])
def receive_order():
    data = request.json
    order_id = data.get('id')
    if not order_id:
        return jsonify({'error': 'Order ID missing'}), 400

    order = {
        'id': order_id,
        'status': 'preparing'
    }
    kitchen_queue.append(order)
    save_kitchen_orders()
    return jsonify({'message': f'Order {order_id} is being prepared'}), 200

@app.route('/kitchen', methods=['GET'])
def get_kitchen_orders():
    return jsonify(kitchen_queue), 200

# Background thread to update order status
def process_orders():
    while True:
        for order in kitchen_queue:
            if order['status'] == 'preparing':
                # Wait for a random time between 5 and 15 seconds
                time.sleep(random.randint(5, 60))
                order['status'] = 'completed'
                print(f"Order {order['id']} is now completed.")
                save_kitchen_orders()
        time.sleep(1)  # Check the queue every second

if __name__ == '__main__':
    load_kitchen_orders()
    # Start the background thread
    threading.Thread(target=process_orders, daemon=True).start()
    app.run(debug=True, port=5002)
