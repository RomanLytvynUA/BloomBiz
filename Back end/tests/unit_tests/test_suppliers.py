from src import db
from src.models.suppliers import Suppliers
from testing_data import add_testing_suppliers, clear_db
from src.utils.suppliers import util_create_supplier, util_edit_supplier


def test_suppliers_generate_dict(app_client):
    """
    GIVEN supplier instance
    WHEN calling generate_dict() method on supplier
    THEN dict with proper data is returned 
    """
    clear_db()
    supplier_data = add_testing_suppliers()[0]
    supplier_obj = Suppliers.query.filter_by(id=1).first()

    assert supplier_obj.generate_dict() == supplier_data


def test_util_create_supplier(app_client):
    """
    GIVEN create supplier util
    WHEN calling create supplier util with unique name
    THEN db contains proper instance of suppliers;
         proper instance of supplier is returned;
    """
    clear_db()
    supplier = util_create_supplier("Test supplier", "-", "--")['supplier']

    queried_supplier = Suppliers.query.filter_by(name="Test supplier").first()

    assert queried_supplier.name == "Test supplier"
    assert queried_supplier.contactInfo == "-"
    assert queried_supplier.additional == "--"


def test_util_create_supplier_clone(app_client):
    """
    GIVEN create_supplier func
    WHEN calling create supplier util with existing name
    THEN new supplier is not added to the db;
         proper instance of supplier is returned;
    """
    clear_db()
    supplier_data = add_testing_suppliers()[0]
    supplier = util_create_supplier(supplier_data['name'])['supplier']

    queried_suppliers = Suppliers.query.filter_by(name=supplier_data['name']).all()

    assert len(queried_suppliers)
    assert supplier == queried_suppliers[0]
    assert queried_suppliers[0].name == supplier_data['name']
    assert queried_suppliers[0].contactInfo == supplier_data['contactInfo']
    assert queried_suppliers[0].additional == supplier_data['additional']


def test_util_edit_supplier(app_client):
    """
    GIVEN supplier instance
    WHEN calling edit supplier util with an id of an exicting supplier
    THEN supplier instance is properly edited;
         edited supplier is returned.
    """
    clear_db()
    supplier_id = add_testing_suppliers()[0]['id']
    edited_supplier = util_edit_supplier(supplier_id, '1', '2', '3')['supplier']
    queried_supplier = Suppliers.query.filter_by(id=supplier_id).first()

    assert queried_supplier.name == "1"
    assert queried_supplier.contactInfo == "2"
    assert queried_supplier.additional == "3"
    assert queried_supplier == edited_supplier


def test_util_edit_supplier_invalid_id(app_client):
    """
    GIVEN supplier instance
    WHEN calling edit supplier util with an invalid id
    THEN None is returned.
    """
    clear_db()
    edited_supplier = util_edit_supplier(1, '1', '2', '3')['supplier']

    assert edited_supplier is None
