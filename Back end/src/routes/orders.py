from .. import db
from flask import jsonify, request, Blueprint
from src.models.orders import Orders, OrdersElements
from src.models.goods import Goods
from src.models.goods import Categories
from src.models.customers import Customers
from ..utils.goods import util_create_product
from ..utils.orders import util_create_order
from ..utils.customers import util_create_customer
from flask_jwt_extended import verify_jwt_in_request


orders = Blueprint("orders", __name__)


@orders.before_request
def before_request_func():
    verify_jwt_in_request()


@orders.route("/get", methods=["GET"])
def get_orders():
    data = [
        order.generate_dict() for order in Orders.query.order_by(Orders.id.desc()).all()
    ]
    return jsonify(data)


@orders.route("/create", methods=["POST"])
def create_order():
    orders_data = request.get_json()

    required_data = {"date", "price", "discount", "status", "elements", "additional"}
    if not len(required_data - set(orders_data.keys())):

        # get customers and address
        order_address = ""
        customer = None
        receiver = None
        if "customer" in orders_data:
            customer = util_create_customer(
                orders_data["customer"].get("name", ""),
                orders_data["customer"].get("contactInfo", ""),
                orders_data["customer"].get("additional", ""),
            )["customer"]
            if "receiver" in orders_data:
                order_address = orders_data["receiver"].get("address", "")
                receiver = util_create_customer(
                    orders_data["receiver"].get("name", ""),
                    orders_data["receiver"].get("contactInfo", ""),
                    orders_data["receiver"].get("additional", ""),
                )["customer"]
            else:
                order_address = orders_data["customer"].get("address", "")
                receiver = customer

        # create order
        order = util_create_order(
            date=orders_data["date"],
            discount=orders_data["discount"],
            status=orders_data["status"],
            price=orders_data["price"],
            customer=customer,
            receiver=receiver,
            address=order_address,
            additional=orders_data["additional"],
        )["order"]

        # add order elements
        for category in orders_data["elements"].keys():
            category_obj = Categories.query.filter_by(name=category).first()
            if not category_obj:
                return f'Failed to fetch the given category "{category}".', 406

            for element in orders_data["elements"][category]:
                new_element = OrdersElements(
                    quantity=element["quantity"],
                    price=element["price"],
                    product=util_create_product(element.get("product"), category_obj)[
                        "product"
                    ],
                    order=order,
                )
                db.session.add(new_element)
        db.session.commit()

        changes = {
            "orders": [order.generate_dict()],
            "customers": [obj.generate_dict() for obj in [customer, receiver] if obj],
            # add all products from order elements since in-stock quantity needs to be recalculated
            "goods": [element.product.generate_dict() for element in order.elements],
        }

        return jsonify(changes), 200
    return "Missing required data.", 406


@orders.route("/edit", methods=["PUT"])
def edit_order():
    orders_data = request.get_json()

    required_data = {"order_id", "date", "price", "discount", "status", "elements"}
    if not len(required_data - set(orders_data.keys())):
        changes = {}

        # find customers and address
        customer_id = None
        receiver_id = None
        order_address = ""
        if "customer" in orders_data:
            customer_id = util_create_customer(
                orders_data["customer"].get("name", ""),
                orders_data["customer"].get("contactInfo", ""),
                orders_data["customer"].get("additional", ""),
            )["customer"].id
            if "receiver" in orders_data:
                order_address = orders_data["receiver"].get("address", "")
                receiver_id = util_create_customer(
                    orders_data["receiver"].get("name", ""),
                    orders_data["receiver"].get("contactInfo", ""),
                    orders_data["receiver"].get("additional", ""),
                )["customer"].id
            else:
                order_address = orders_data["customer"].get("address", "")
                receiver_id = customer_id

        # change order fields
        order = Orders.query.filter_by(id=orders_data["order_id"]).first()
        if not order:
            return f"Failed to fetch the given order.", 406
        order.date = orders_data["date"]
        order.price = orders_data["price"]
        order.status = orders_data["status"]
        order.discount = orders_data["discount"]
        order.additional = orders_data["additional"]
        # add old customers to changes
        changes["customers"] = [
            Customers.query.filter_by(id=id).first().generate_dict()
            for id in [order.receiver_id, order.customer_id]
            if id
        ]
        order.customer_id = customer_id
        order.receiver_id = receiver_id
        order.customer_address = order_address
        db.session.add(order)

        # delete old elements
        deleted_products_id = []
        for element in OrdersElements.query.filter_by(order=order).all():
            db.session.delete(element)
        db.session.commit()

        # add deleted elements to changes so that the in-stock quantity is recalculated
        deleted_goods = Goods.query.filter(Goods.id.in_(deleted_products_id)).all()
        changes["goods"] = [product.generate_dict() for product in deleted_goods]

        # add order elements
        for category in orders_data["elements"].keys():
            category_obj = Categories.query.filter_by(name=category).first()
            if not category_obj:
                return f'Failed to fetch the given category "{category}".', 406

            for element in orders_data["elements"][category]:
                new_element = OrdersElements(
                    quantity=element["quantity"],
                    price=element["price"],
                    product=util_create_product(element.get("product"), category_obj)[
                        "product"
                    ],
                    order=order,
                )
                db.session.add(new_element)
        db.session.commit()

        # must add order to changes only after adding elements
        changes["orders"] = [order.generate_dict()]

        # add all products from order elements to changes since in-stock qunatity needs to be recalculated
        for element in order.elements:
            # remove old product from changes if it is there
            for product_changed in changes["goods"]:
                if product_changed["id"] == element.product.id:
                    changes["goods"].remove(product_changed)
                    break
            changes["goods"].append(element.product.generate_dict())

        # add new customers
        changes["customers"] = changes["customers"] + [
            Customers.query.filter_by(id=id).first().generate_dict()
            for id in [order.receiver_id, order.customer_id]
            if id
        ]

        return jsonify(changes), 200
    return "Missing required data.", 406


@orders.route("/delete/<expense_id>", methods=["DELETE"])
def delete_order(expense_id):
    order = Orders.query.filter_by(id=expense_id).all()

    if len(order):
        db.session.delete(order[0])
        db.session.commit()

        return "Order deleted successfully.", 200
    return "Failed to fetch the order with given id.", 400
