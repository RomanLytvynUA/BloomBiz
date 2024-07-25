from src import db
from flask import jsonify, Blueprint, request
from src.models.goods import Categories, Goods, Decommissions
from src.utils.goods import (
    util_calc_instock,
    util_create_product,
    util_create_category,
    util_create_decommission,
    util_set_product_price,
)
from flask_jwt_extended import verify_jwt_in_request


goods = Blueprint("goods", __name__)


@goods.before_request
def before_request_func():
    verify_jwt_in_request()


@goods.route("/get", methods=["GET"])
def get_goods():
    data = [
        category.generate_dict()
        for category in Categories.query.order_by(Categories.id).all()
    ]
    return jsonify(data)


@goods.route("/create_product", methods=["POST"])
def create_product():
    data = request.get_json()

    required_data = {"product", "category"}
    if not len(required_data - set(data.keys())):
        product = data["product"]

        category = Categories.query.filter_by(name=data["category"]).first()
        if not category:
            return "Invalid category", 406

        result = util_create_product(name=product, category=category)
        changes = {
            "goods": (
                [result["product"].generate_dict()] if result["changes_applied"] else []
            )
        }
        return jsonify(changes), 201
    return "Missing required data.", 406


@goods.route("/edit_product", methods=["PUT"])
def edit_product():
    data = request.get_json()

    required_data = {"product_id", "name"}
    if not len(required_data - set(data.keys())):
        product = Goods.query.filter_by(id=data["product_id"]).first()
        if not product:
            return "Invalid product", 406

        product.name = data["name"]
        db.session.add(product)
        db.session.commit()

        changes = {"goods": [product.generate_dict()]}

        return jsonify(changes), 201
    return "Missing required data.", 406


@goods.route("/delete_product/<product_id>", methods=["DELETE"])
def delete_product(product_id):
    product = Goods.query.filter_by(id=product_id).first()

    if product:
        db.session.delete(product)
        db.session.commit()

        return "Product deleted successfully.", 200
    return "Failed to fetch the product with given id.", 406


@goods.route("/create_category", methods=["POST"])
def create_category():
    data = request.get_json()

    required_data = {"categoryUnits", "category"}
    if not len(required_data - set(data.keys())):
        category = data["category"]
        units = data["categoryUnits"]

        result = util_create_category(name=category, units=units)

        changes = {
            "categories": (
                [result["category"].generate_dict()]
                if result["changes_applied"]
                else []
            )
        }
        return jsonify(changes), 201
    return "Missing required data.", 406


@goods.route("/edit_category", methods=["PUT"])
def edit_category():
    data = request.get_json()

    required_data = {"targetCategory", "category", "categoryUnits"}
    if not len(required_data - set(data.keys())):
        category = Categories.query.filter_by(name=data["targetCategory"]).first()
        if not category:
            return "Invalid category.", 406

        category.name = data["category"]
        category.units = data["categoryUnits"]
        db.session.add(category)
        db.session.commit()

        changes = {"categories": [category.generate_dict()]}

        return jsonify(changes), 201
    return "Missing required data.", 406


@goods.route("/delete_category/<category_id>", methods=["DELETE"])
def delete_category(category_id):
    category = Categories.query.filter_by(id=category_id).first()

    if category:
        db.session.delete(category)
        db.session.commit()

        return "Category deleted successfully.", 200
    return "Failed to fetch the category with given id.", 406


@goods.route("/edit_price", methods=["POST"])
def edit_goods_price():
    data = request.get_json()

    required_data = {"product_id", "price"}
    if not len(required_data - set(data.keys())):
        price = data["price"]
        product_id = data["product_id"]

        result = util_set_product_price(product_id=product_id, price=price)

        changes = {
            "goods": (
                [Goods.query.filter_by(id=product_id).first().generate_dict()]
                if result["changes_applied"]
                else []
            )
        }

        return jsonify(changes), 200
    return "Missing required data.", 406


@goods.route("/reset_prices", methods=["POST"])
def reset_goods_prices():
    Goods.query.update({Goods.price: None})
    db.session.commit()

    return "Reset prices successfuly.", 200


@goods.route("/get_decommissions", methods=["GET"])
def get_decommissions():
    data = [decommission.generate_dict() for decommission in Decommissions.query.all()]
    return jsonify(data)


@goods.route("/create_decommission", methods=["POST"])
def create_decommission():
    data = request.get_json()
    required_data = {"date", "productId", "quantity"}
    if not len(required_data - set(data.keys())):
        product = Goods.query.filter_by(id=data["productId"]).first()
        if not product:
            return "Failed to fetch product with provided id.", 400

        result = util_create_decommission(
            date=data["date"], product=product, quantity=data["quantity"]
        )

        changes = {"goods": [product.generate_dict()]}

        return jsonify(changes), 200
    return "Missing required data.", 406


@goods.route("/delete_decommission/<decommission_id>", methods=["DELETE"])
def delete_decommission(decommission_id):
    decommission = Decommissions.query.filter_by(id=decommission_id).all()

    if len(decommission):
        db.session.delete(decommission[0])
        db.session.commit()

        return "Decommission deleted successfully.", 200
    return "Failed to fetch the decommission with given id.", 406
