from flask import Flask, request, jsonify

app = Flask(__name__)

# Simulates orders in the kitchen
kitchen_queue = []

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
    return jsonify({'message': f'Order {order_id} is being prepared'}), 200

@app.route('/kitchen', methods=['GET'])
def get_kitchen_orders():
    return jsonify(kitchen_queue), 200

if __name__ == '__main__':
    app.run(debug=True, port=5002)
