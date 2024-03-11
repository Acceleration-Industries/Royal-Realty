from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from exotic_builds_garage.models import Customer, Product, ProdOrder, Order, db, product_schema, products_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/token', methods=['GET', 'POST'])
def token():
    data = request.json
    if data:
        client_id = data['client_id']
        access_token = create_access_token(identity=client_id)
        return {'status': 200, 'access_token': access_token}
    else:
        return {'status': 400, 'message': 'Missing Client Id. Try Again.'}

@api.route('/shop')
@jwt_required()
def get_shop():
    allprods = Product.query.all()
    response = products_schema.dump(allprods)
    return jsonify(response)

@api.route('/order/create/<cust_id>', methods=['POST'])
@jwt_required()
def create_order(cust_id):
    data = request.json
    customer_order = data['order']
    customer = Customer.query.filter(Customer.cust_id == cust_id).first()
    if not customer:
        customer = Customer(cust_id)
        db.session.add(customer)
    order = Order()
    db.session.add(order)
    for product in customer_order:
        prodorder = ProdOrder(product['prod_id'], product['quantity'], product['price'], order.order_id, cust_id)
        db.session.add(prodorder)
        order.increment_ordertotal(prodorder.price)
        current_product = Product.query.get(product['prod_id'])
        current_product.decrement_quantity(product['quantity'])
    db.session.commit()
    return {'status': 200, 'message': 'New Order was Created'}

@api.route('/order/<cust_id>')
@jwt_required()
def get_orders(cust_id):
    prodorder = ProdOrder.query.filter(ProdOrder.cust_id == cust_id).all()
    data = []
    for order in prodorder:
        product = Product.query.filter(Product.prod_id == order.prod_id).first()
        product_dict = product_schema.dump(product)
        product_dict['quantity'] = order.quantity
        product_dict['order_id'] = order.order_id
        product_dict['id'] = order.prodorder_id
        data.append(product_dict)
    return jsonify(data)

@api.route('/order/update/<order_id>', methods=['PUT'])
@jwt_required()
def update_order(order_id):
    data = request.json
    new_quantity = int(data['quantity'])
    prod_id = data['prod_id']
    prodorder = ProdOrder.query.filter(ProdOrder.order_id == order_id, ProdOrder.prod_id == prod_id).first()
    order = Order.query.get(order_id)
    product = Product.query.get(prod_id)
    order.decrement_ordertotal(prodorder.price)
    prodorder.set_price(product.price, new_quantity)
    order.increment_ordertotal(prodorder.price)
    diff = abs(new_quantity - prodorder.quantity)
    if prodorder.quantity > new_quantity:
        product.increment_quantity(diff)
    else:
        product.decrement_quantity(diff)
    prodorder.update_quantity(new_quantity)
    db.session.commit()
    return {'status': 200, 'message': 'Order was Updated Successfully'}

@api.route('/order/delete/<order_id>', methods=['DELETE'])
@jwt_required()
def delete_order(order_id):
    data = request.json
    prod_id = data['prod_id']
    prodorder = ProdOrder.query.filter(ProdOrder.order_id == order_id, ProdOrder.prod_id == prod_id).first()
    order = Order.query.get(order_id)
    product = Product.query.get(prod_id)
    order.decrement_ordertotal(prodorder.price)
    product.increment_quantity(prodorder.quantity)
    db.session.delete(prodorder)
    db.session.commit()
    return {'status': 200, 'message': 'Order was Successfully Deleted'}
# @site.route('/shop/makes')
# def shop_makes():
#     return render_template('makes.html')

# @site.route('/shop/makes/porsche')
# def porsche():
#     return render_template('porsche.html')

# @site.route('/shop/makes/pagani')
# def pagani():
#     return render_template('pagani.html')

# @site.route('/shop/makes/mercedes')
# def mercedes():
#     return render_template('mercedes.html')

# @site.route('/shop/makes/mclaren')
# def mclaren():
#     return render_template('mclaren.html')

# @site.route('/shop/makes/maserati')
# def maserati():
#     return render_template('maserati.html')

# @site.route('/shop/makes/lexus')
# def lexus():
#     return render_template('lexus.html')

# @site.route('/shop/makes/lamborghini')
# def lamborghini():
#     return render_template('lamborghini.html')

# @site.route('/shop/makes/koenigsegg')
# def koenigsegg():
#     return render_template('koenigsegg.html')

# @site.route('/shop/makes/jaguar')
# def jaguar():
#     return render_template('jaguar.html')

# @site.route('/shop/makes/hennessey')
# def hennessey():
#     return render_template('hennessey.html')

# @site.route('/shop/makes/ferrari')
# def ferrari():
#     return render_template('ferrari.html')

# @site.route('/contact_us')
# def contact_us():
#     return render_template('contact_us.html')

# @site.route('/clothing')
# def clothing():
#     return render_template('clothing.html')

# @site.route('/cart')
# def cart():
#     return render_template('cart.html')

# @site.route('/cars_for_sale')
# def cars_for_sale():
#     return render_template('cars_for_sale.html')

# @site.route('/shop/makes/bugatti')
# def bugatti():
#     return render_template('bugatti.html')

# @site.route('/shop/makes/bmw')
# def bmw():
#     return render_template('bmw.html')

# @site.route('/shop/makes/audi')
# def audi():
#     return render_template('audi.html')

# @site.route('/shop/makes/astonmartin')
# def astonmartin():
#     return render_template('astonmartin.html')
