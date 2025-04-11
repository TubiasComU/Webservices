from flask import Flask, request, jsonify

app = Flask(__name__)

# Simulates payment transactions
payments = []

@app.route('/payments', methods=['POST'])
def process_payment():
    data = request.json
    order_id = data.get('order_id')
    amount = data.get('amount')

    if not order_id or not amount:
        return jsonify({'error': 'Missing order_id or amount'}), 400

    payment = {
        'order_id': order_id,
        'amount': amount,
        'status': 'paid'
    }
    payments.append(payment)
    return jsonify({'message': 'Payment successful'}), 200

@app.route('/payments', methods=['GET'])
def get_payments():
    return jsonify(payments), 200

if __name__ == '__main__':
    app.run(debug=True, port=5003)
