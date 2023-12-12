from flask import request, jsonify
from datetime import datetime
from dbsetup import app, db
from models.order import Order
from models.product import Product
from models.invoice import Invoice

# Реалізація ендпоінтів
@app.route('/products', methods=['GET'])
def get_products():
    """
    Get the list of products
    ---
    responses:
      200:
        description: A list of products
    """
    products = Product.query.all()
    result = [{'id': product.id, 'name': product.name, 'price': product.price} for product in products]
    return jsonify(result)

@app.route('/products', methods=['POST'])
def create_product():
    """
    Create a new product
    ---
    parameters:
      - name: name
        in: formData
        type: string
        required: true
        description: Name of the product
      - name: price
        in: formData
        type: float
        required: true
        description: Price of the product
    responses:
      201:
        description: Product created successfully
    """
    data = request.form
    product = Product(name=data['name'], price=data['price'])
    db.session.add(product)
    db.session.commit()

    return jsonify({'message': 'Product created successfully'}), 201

@app.route('/orders', methods=['GET'])
def get_orders():
    """
    Get the list of orders
    ---
    responses:
      200:
        description: A list of orders
    """
    orders = Order.query.all()
    result = [{'id': order.id, 'product_id': order.product_id, 'status': order.status, 'created_at': order.created_at} for order in orders]
    return jsonify(result)

@app.route('/orders', methods=['POST'])
def create_order():
    """
    Create a new order
    ---
    parameters:
      - name: product_id
        in: formData
        type: integer
        required: true
        description: ID of the product for the order
    responses:
      201:
        description: Order created successfully
    """
    data = request.form
    product = Product.query.get(data['product_id'])
    if not product:
        return jsonify({'message': 'Product not found'}), 404

    order = Order(product_id=data['product_id'])
    db.session.add(order)
    db.session.commit()

    return jsonify({'message': 'Order created successfully'}), 201

@app.route('/orders/complete/<int:order_id>', methods=['PUT'])
def complete_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'message': 'Order not found'}), 404

    order.status = 'completed'
    db.session.commit()

    return jsonify({'message': 'Order processed successfully'}), 200

@app.route('/orders/paid/<int:order_id>', methods=['PUT'])
def paid_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'message': 'Order not found'}), 404

    order.status = 'paid'
    db.session.commit()

    return jsonify({'message': 'Order processed successfully'}), 200

@app.route('/invoices', methods=['GET'])
def get_invoices():
    """
    Get the list of invoices
    ---
    responses:
      200:
        description: A list of invoices
    """
    invoices = Invoice.query.all()
    result = [
        {
            'id': invoice.id,
            'order_id': invoice.order_id,
            'total_price': invoice.total_price,
            'product_name': invoice.product_name,
            'product_price': invoice.product_price,
            'created_at': invoice.created_at
        } for invoice in invoices
    ]
    return jsonify(result)

@app.route('/invoices', methods=['POST'])
def create_invoice():
    """
    Create a new invoice
    ---
    parameters:
      - name: order_id
        in: query
        type: integer
        required: true
        description: ID of the order for the invoice
      - name: product_id
        in: query
        type: integer
        required: true
        description: ID of the product for the invoice
      - name: total_price
        in: formData
        type: float
        required: true
        description: Total price of the invoice
    responses:
      201:
        description: Invoice created successfully
    """
    order_id = request.args.get('order_id')
    product_id = request.args.get('product_id')
    
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'message': 'Order not found'}), 404

    product = Product.query.get(product_id)
    if not product:
        return jsonify({'message': 'Product not found'}), 404

    total_price = float(request.form['total_price'])

    invoice = Invoice(
        order_id=order_id,
        total_price=total_price,
        product_name=product.name,
        product_price=product.price
    )
    db.session.add(invoice)
    db.session.commit()

    return jsonify({'message': 'Invoice created successfully'}), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
