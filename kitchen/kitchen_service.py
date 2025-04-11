from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

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
    print(f"[Kitchen] Pedido {order_id} adicionado à fila")
    return jsonify({'message': f'Order {order_id} is being prepared'}), 200

@app.route('/kitchen', methods=['GET'])
def get_kitchen_orders():
    return jsonify(kitchen_queue), 200

if __name__ == '__main__':
    load_kitchen_orders()
    app.run(debug=True, port=5002)
