from flask import Flask, request, jsonify
import json
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

ORDERS_FILE = 'orders/orders.json'
orders = []
next_id = 1

# Load orders from JSON file
def load_orders():
    global orders, next_id
    if os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, 'r') as f:
            orders = json.load(f)
            if orders:
                next_id = max(order["id"] for order in orders) + 1

# Save orders to JSON file
def save_orders():
    with open(ORDERS_FILE, 'w') as f:
        json.dump(orders, f, indent=2)

@app.route('/orders', methods=['POST'])
def create_order():
    global next_id
    data = request.json
    order = {
        "id": next_id,
        "table": data.get("table"),
        "items": data.get("items", []),
        "status": "pending"
    }
    orders.append(order)
    next_id += 1
    save_orders()
    return jsonify(order), 201

@app.route('/orders', methods=['GET'])
def list_orders():
    return jsonify(orders), 200

@app.route('/orders/<int:order_id>', methods=['PATCH'])
def update_order_status(order_id):
    data = request.json
    for order in orders:
        if order["id"] == order_id:
            order["status"] = data.get("status", order["status"])
            save_orders()
            return jsonify(order), 200
    return jsonify({"error": "Order not found"}), 404

@app.route('/orders/table/<int:table>', methods=['DELETE'])
def delete_orders_by_table(table):
    global orders
    orders = [o for o in orders if o["table"] != table]
    save_orders()
    return jsonify({"message": f"Orders for table {table} deleted"}), 200


if __name__ == '__main__':
    load_orders()
    app.run(debug=True, port=5001)
