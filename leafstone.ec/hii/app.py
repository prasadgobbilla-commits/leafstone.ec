from flask import Flask, jsonify

app = Flask(__name__)

# Sample orders
orders = [
    {"id": 1, "product": "Product A", "qty": 2, "price": 500},
    {"id": 2, "product": "Product B", "qty": 1, "price": 300},
    {"id": 3, "product": "Product C", "qty": 5, "price": 1500}
]

@app.route('/orders')
def get_orders():
    return jsonify(orders)

if __name__ == '__main__':
    app.run(debug=True)
