import json
import requests
from src.models.suppliers import Suppliers
from tests.testing_data import clear_db, add_testing_suppliers


def test_get_suppliers(urls, jwt):
    """
    GIVEN db with a supplier instance
    WHEN calling get suppliers endpoint
    THEN proper data is returned
    """
    route = urls["get_suppliers"]

    clear_db()
    suppliers = add_testing_suppliers()

    response = requests.get(
        url=route["route"], headers={"Authorization": f"Bearer {jwt}"}
    )

    assert json.loads(response.text) == suppliers


def test_create_supplier(urls, app_client, jwt):
    """
    GIVEN create supplier endpoint
    WHEN calling create supplier endpoint
    THEN new supplier is added;
         proper changes are returned.
    PROVIDED all required data is present
    """
    route = urls["create_supplier"]

    clear_db()
    data = {"name": "Supplier", "contactInfo": "phone number", "additional": "comment"}
    positive_response = requests.post(
        url=route["route"],
        json=data,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {jwt}"},
    )
    negative_response = requests.post(
        url=route["route"],
        json={},
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {jwt}"},
    )

    supplier = Suppliers.query.filter_by(
        name=data["name"],
        contactInfo=data["contactInfo"],
        additional=data["additional"],
    ).all()

    assert "suppliers" in json.loads(positive_response.text)
    assert positive_response.status_code == 200
    assert negative_response.status_code == 406
    assert len(supplier)


def test_edit_supplier(urls, app_client, jwt):
    """
    GIVEN db with a supplier instance
    WHEN calling edit supplier endpoint
    THEN supplier is edited;
         proper changes are returned.
    PROVIDED all required data is present
    """
    route = urls["edit_supplier"]

    clear_db()
    supplier_data = add_testing_suppliers()[0]
    data = {
        "id": supplier_data["id"],
        "name": "Supplier1",
        "contactInfo": "phone number1",
        "additional": "comment1",
    }
    positive_response = requests.put(
        url=route["route"],
        json=data,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {jwt}"},
    )
    negative_response = requests.put(
        url=route["route"],
        json={},
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {jwt}"},
    )

    supplier = Suppliers.query.filter_by(
        id=supplier_data["id"],
        name=data["name"],
        contactInfo=data["contactInfo"],
        additional=data["additional"],
    ).all()

    assert "suppliers" in json.loads(positive_response.text)
    assert positive_response.status_code == 200
    assert negative_response.status_code == 406
    assert len(supplier)


def test_del_supplier(urls, app_client, jwt):
    """
    GIVEN db with a supplier instance
    WHEN calling delete supplier endpoint
    THEN supplier is deleted
    """
    route = urls["del_supplier"]

    clear_db()
    supplier_data = add_testing_suppliers()[0]
    response = requests.delete(
        url=route["route"] + str(supplier_data["id"]),
        headers={"Authorization": f"Bearer {jwt}"},
    )
    supplier = Suppliers.query.filter_by(id=supplier_data["id"]).all()

    assert response.status_code == 200
    assert not len(supplier)
