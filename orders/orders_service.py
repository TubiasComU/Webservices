from flask import Flask, request, jsonify

app = Flask(__name__)

orders = []
next_id = 1

@app.route('/orders', methods=['POST'])
def create_order():
    global next_id
    data = request.json
    order = {
        "id": next_id,
        "items": data.get("items", []),
        "status": "pending"
    }
    orders.append(order)
    next_id += 1
    print(f"[Orders] Nova ordem criada: {order}")
    return jsonify(order), 201

@app.route('/orders', methods=['GET'])
def list_orders():
    return jsonify(orders), 200

# PATCH method to update order status
@app.route('/orders/<int:order_id>', methods=['PATCH'])
def update_order_status(order_id):
    data = request.json
    for order in orders:
        if order["id"] == order_id:
            order["status"] = data.get("status", order["status"])
            print(f"[Orders] Ordem {order_id} atualizada para: {order['status']}")
            return jsonify(order), 200
    return jsonify({"error": "Order not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5001)
