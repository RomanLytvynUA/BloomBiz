from .. import db
from flask import jsonify, request, Blueprint
from ..models.customers import Customers
from ..utils.customers import util_create_customer, util_edit_customer

customers = Blueprint("customers", __name__)


@customers.route('/get', methods=['GET'])
def get_customers():
    data = [customer.generate_dict() for customer in Customers.query.order_by(Customers.id.desc()).all()]

    return jsonify(data)


@customers.route('/create', methods=['POST'])
def create_customer():
    customer_data = request.get_json()
    required_data = {'name', 'additional', 'contactInfo'}
    if not len(required_data - set(customer_data.keys())):
        result = util_create_customer(customer_data['name'], customer_data['contactInfo'], customer_data['additional'])

        return result['message'], 200
    return "Missing required data.", 406


@customers.route('/edit', methods=['PUT'])
def edit_customer():
    customer_data = request.get_json()
    required_data = {'name', 'additional', 'contactInfo', 'id'}
    if not len(required_data - set(customer_data.keys())):
        
        result = util_edit_customer(customer_data['id'], customer_data['name'],
                                    customer_data['contactInfo'], customer_data['additional'])

        return result['message'], 200
    return "Missing required data.", 406


@customers.route('/delete/<customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    customer = Customers.query.filter_by(id=customer_id).all()

    if len(customer):
        db.session.delete(customer[0])
        db.session.commit()

        return "Customer deleted successfully.", 200
    return "Failed to fetch customer with given id.", 400
