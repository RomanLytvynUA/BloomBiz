from src import db
from flask import jsonify, Blueprint, request
from src.models.goods import Categories, Goods, Decommissions
from src.utils.goods import util_calc_instock, util_create_product, util_create_category, util_create_decommission,\
    util_set_product_price


goods = Blueprint("goods", __name__)


@goods.route('/get', methods=['GET'])
def get_goods():
    data = [category.generate_dict() for category in Categories.query.order_by(Categories.id).all()]
    return jsonify(data)


@goods.route('/edit_price', methods=['POST'])
def edit_goods_price():
    data = request.get_json()

    required_data = {'product_id', 'price'}
    if not len(required_data - set(data.keys())):
        price = data['price']
        product_id = data['product_id']

        result = util_set_product_price(product_id=product_id, price=price)

        if 'Set price successfully.' == result['message']:
            return 'Set price successfully.', 200
        return result['message'], 400
    return "Missing required data.", 406


@goods.route('/get_instock', methods=['GET'])
def get_instock():
    data = util_calc_instock()
    return jsonify(data)


@goods.route('/get_decommissions', methods=['GET'])
def get_decommissions():
    data = [decommission.generate_dict() for decommission in Decommissions.query.all()]
    return jsonify(data)


@goods.route('/create_decommission', methods=['POST'])
def create_decommission():
    data = request.get_json()

    required_data = {'date', 'product', "category", 'quantity'}
    if not len(required_data - set(data.keys())):
        date = data['date']
        quantity = data['quantity']
        product = data['product']
        category = data['category']

        result = util_create_decommission(date=date, product=product, quantity=quantity, category=str(category))

        if "decommission" in result.keys():
            return result['message'], 200
        return result['message'], 424
    return "Missing required data.", 406


@goods.route('/delete_decommission/<decommission_id>', methods=['DELETE'])
def delete_decommission(decommission_id):
    decommission = Decommissions.query.filter_by(id=decommission_id).all()

    if len(decommission):
        db.session.delete(decommission[0])
        db.session.commit()

        return "Decommission deleted successfully.", 200
    return "Failed to fetch the decommission with given id.", 406
