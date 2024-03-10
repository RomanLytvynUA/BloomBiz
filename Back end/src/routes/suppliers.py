from .. import db
from flask import jsonify, request, Blueprint
from ..models.suppliers import Suppliers
from ..utils.suppliers import util_edit_supplier, util_create_supplier

suppliers = Blueprint("suppliers", __name__)


@suppliers.route('/get', methods=['GET'])
def get_suppliers():
    data = [supplier.generate_dict() for supplier in Suppliers.query.order_by(Suppliers.id.desc()).all()]

    return jsonify(data)


@suppliers.route('/create', methods=['POST'])
def create_supplier():
    supplier_data = request.get_json()
    required_data = {'name', 'additional', 'contactInfo'}
    if not len(required_data - set(supplier_data.keys())):
        result = util_create_supplier(supplier_data['name'], supplier_data['contactInfo'], supplier_data['additional'])

        return result['message'], 200
    return "Missing required data.", 406


@suppliers.route('/edit', methods=['PUT'])
def edit_supplier():
    supplier_data = request.get_json()
    required_data = {'name', 'id', 'additional', 'contactInfo'}
    if not len(required_data - set(supplier_data.keys())):
        result = util_edit_supplier(supplier_data['id'], supplier_data['name'],
                                    supplier_data['contactInfo'], supplier_data['additional'])

        return result['message'], 200
    return "Missing required data.", 406


@suppliers.route('/delete/<supplier_id>', methods=['DELETE'])
def delete_supplier(supplier_id):
    supplier = Suppliers.query.filter_by(id=supplier_id).all()

    if len(supplier):
        db.session.delete(supplier[0])
        db.session.commit()

        return "Supplier deleted successfully.", 200
    return "Failed to fetch the supplier with given id.", 400
