from flask import Flask, request, jsonify

app = Flask(__name__)

# Temporary store of the orders (depois trocar por uma base de dados ou nao)
orders = []

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    order_id = len(orders) + 1
    order = {
        'id': order_id,
        'items': data.get('items', []),
        'status': 'received'
    }
    orders.append(order)
    return jsonify(order), 201

@app.route('/orders', methods=['GET'])
def get_orders():
    return jsonify(orders), 200

if __name__ == '__main__':
    app.run(debug=True, port=5001)
