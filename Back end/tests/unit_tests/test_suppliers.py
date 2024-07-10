from src import db
from src.models.suppliers import Suppliers
from testing_data import add_testing_suppliers, clear_db
from src.utils.suppliers import util_create_supplier, util_edit_supplier


def test_suppliers_generate_dict(app_client):
    """
    GIVEN supplier instance
    WHEN calling generate_dict() method of supplier
    THEN dict with proper data is returned.
    """
    clear_db()
    supplier_data = add_testing_suppliers()[0]
    supplier_obj = Suppliers.query.filter_by(id=1).first()

    assert supplier_obj.generate_dict() == supplier_data


def test_util_create_supplier(app_client):
    """
    GIVEN create supplier util
    WHEN calling create supplier util with a unique name
    THEN db contains proper instance of supplier;
         output contains proper instance of supplier;
         output contains changes_applied set to true.
    """
    clear_db()

    output = util_create_supplier("Test supplier", "-", "--")
    queried_supplier = Suppliers.query.filter_by(
        name="Test supplier", contactInfo="-", additional="--"
    ).first()

    assert queried_supplier
    assert output["supplier"] == queried_supplier
    assert output["changes_applied"] == True


def test_util_create_supplier_clone(app_client):
    """
    GIVEN supplier instance
    WHEN calling create supplier util with an existing name
    THEN new supplier is not added to the db;
         output contains existing instance of supplier;
         output contains changes_applied set to false.
    """
    clear_db()

    supplier_data = add_testing_suppliers()[0]

    output = util_create_supplier(supplier_data["name"])
    queried_suppliers = Suppliers.query.filter_by(name=supplier_data["name"]).all()

    assert len(queried_suppliers) == 1
    assert output["supplier"] == queried_suppliers[0]
    assert output["changes_applied"] == False


def test_util_edit_supplier(app_client):
    """
    GIVEN supplier instance
    WHEN calling edit supplier util with an id of an exicting supplier
    THEN supplier instance is properly edited;
         output contains edited instance of supplier;
         output contains changes_applied set to true.
    """
    clear_db()

    supplier_id = add_testing_suppliers()[0]["id"]

    output = util_edit_supplier(supplier_id, "1", "2", "3")
    queried_supplier = Suppliers.query.filter_by(id=supplier_id).first()

    assert queried_supplier.name == "1"
    assert queried_supplier.contactInfo == "2"
    assert queried_supplier.additional == "3"
    assert output["supplier"] == queried_supplier
    assert output["changes_applied"] == True


def test_util_edit_supplier_invalid_id(app_client):
    """
    GIVEN supplier instance
    WHEN calling edit supplier util with an invalid id
    THEN output contains None as supplier;
         output contains changes_applied set to false.
    """
    clear_db()

    output = util_edit_supplier(1, "1", "2", "3")

    assert output["supplier"] is None
    assert output["changes_applied"] == False
