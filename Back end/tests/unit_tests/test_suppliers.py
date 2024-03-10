from src import db
from src.models.suppliers import Suppliers
from src.utils.suppliers import util_create_supplier, util_edit_supplier


def test_suppliers_generate_dict(app_client):
    """
    GIVEN supplier instance
    WHEN calling generate_dict() method on supplier
    THEN it returns dict with proper data
    """
    supplier = Suppliers(name="Test supplier", contactInfo="-", additional='--')
    db.session.add(supplier)
    db.session.commit()

    assert supplier.generate_dict() == {'id': supplier.id,
                                        'name': "Test supplier",
                                        'contactInfo': "-",
                                        'additional': "--",
                                        }


def test_util_create_supplier(app_client):
    """
    GIVEN create_supplier func
    WHEN calling create_supplier
    THEN db contains proper instance of suppliers;
         new instance isn't added provided that such name already exists;
         function returns proper instances of suppliers;
    """
    supplier1 = util_create_supplier("Test supplier", "-", "--")['supplier']
    supplier2 = util_create_supplier("Test supplier", "-", "--")['supplier']

    suppliers = list(Suppliers.query.filter_by(name="Test supplier").all())

    assert suppliers[0].name == "Test supplier"
    assert len(suppliers) == 1
    assert suppliers[0] == supplier1
    assert suppliers[0] == supplier2


def test_util_edit_supplier(app_client):
    """
    GIVEN supplier instance
    WHEN calling edit_supplier
    THEN supplier instance gets properly edited;
         func returns None if id is invalid;
    """
    supplier = Suppliers(name="Test supplier", contactInfo="-", additional='--')
    db.session.add(supplier)
    db.session.commit()

    edited_supplier = util_edit_supplier(supplier.id, "Edited name", "Edited contact", "Edited additional")['supplier']
    invalid_supplier = util_edit_supplier(55555, "", "", "")['supplier']

    assert supplier.name == "Edited name"
    assert supplier.contactInfo == "Edited contact"
    assert supplier.additional == "Edited additional"
    assert supplier == edited_supplier
    assert invalid_supplier is None
