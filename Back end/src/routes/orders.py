from .. import db
from flask import jsonify, request, Blueprint
from src.models.orders import Orders, OrdersElements
from src.models.goods import Categories
from ..utils.suppliers import util_create_supplier
from ..utils.goods import util_create_category, util_create_product
from ..utils.orders import util_create_order

orders = Blueprint("orders", __name__)


@orders.route('/get', methods=['GET'])
def get_orders():
    data = [order.generate_dict() for order in Orders.query.order_by(Orders.id.desc()).all()]
    return jsonify(data)


@orders.route('/create', methods=['POST'])
def create_order():
    orders_data = request.get_json()

    required_data = {'date', 'price', 'discount', 'status', "elements"}
    if not len(required_data - set(orders_data.keys())):
        date = orders_data['date']
        price = orders_data['price']
        status = orders_data['status']
        discount = orders_data['discount']
        order_elements = orders_data['elements']

        order = util_create_order(date=date, discount=discount, status=status, price=price)['order']

        # Looping through each element of a copy of order elements list where product string is either
        # replaced with an existing object of goods or fresh created one.
        for category in order_elements.keys():
            category_obj = Categories.query.filter_by(name=category).first()
            if not category_obj:
                return f"Failed to fetch the given category \"{category}\".", 406
            for element in [dict(element, product=util_create_product(element.get('product'), category_obj)['product'])
                            for element in order_elements[category]]:
                new_element = OrdersElements(quantity=element['quantity'], price=element['price'],
                                             product=element['product'], order=order)
                db.session.add(new_element)
        db.session.commit()

        return "Created new order successfully.", 200
    return "Missing required data.", 406


@orders.route('/edit', methods=['PUT'])
def edit_order():
    orders_data = request.get_json()

    required_data = {'order_id', 'date', 'price', 'discount', 'status', "elements"}
    if not len(required_data - set(orders_data.keys())):
        date = orders_data['date']
        price = orders_data['price']
        status = orders_data['status']
        discount = orders_data['discount']
        order_elements = orders_data['elements']

        order = Orders.query.filter_by(id=orders_data['order_id']).first()
        if not order: return f"Failed to fetch the given order.", 406
        order.date = date
        order.price = price
        order.status = status
        order.discount = discount
        db.session.add(order)

        for element in OrdersElements.query.filter_by(order=order).all():
            db.session.delete(element)

        # Looping through each element of a copy of order elements list where product string is either
        # replaced with an existing object of goods or fresh created one.
        for category in order_elements.keys():
            category_obj = Categories.query.filter_by(name=category).first()
            if not category_obj:
                return f"Failed to fetch the given category \"{category}\".", 406
            for element in [dict(element, product=util_create_product(element.get('product'), category_obj)['product'])
                            for element in order_elements[category]]:
                new_element = OrdersElements(quantity=element['quantity'], price=element['price'],
                                             product=element['product'], order=order)
                db.session.add(new_element)
        db.session.commit()

        return "Edited order successfully.", 200
    return "Missing required data.", 406


@orders.route('/delete/<expense_id>', methods=['DELETE'])
def delete_order(expense_id):
    order = Orders.query.filter_by(id=expense_id).all()

    if len(order):
        db.session.delete(order[0])
        db.session.commit()

        return "Order deleted successfully.", 200
    return "Failed to fetch the order with given id.", 400
