import json
import requests
from src.models.customers import Customers
from tests.testing_data import clear_db, add_testing_customers


def test_get_customers(urls, app_client, jwt):
    """
    GIVEN db with a customers instance
    WHEN calling get customers endpoint
    THEN proper data is returned
    """
    route = urls["get_customers"]

    clear_db()
    customers = [
        Customers.query.filter_by(id=customer_data["id"]).first().generate_dict()
        for customer_data in add_testing_customers()
    ]

    response = requests.request(
        url=route["route"],
        method=route["method"],
        headers={"Authorization": f"Bearer {jwt}"},
    )

    assert json.loads(response.text) == customers


def test_create_customer(urls, app_client, jwt):
    """
    GIVEN create customer endpoint
    WHEN calling create customer endpoint
    THEN new customer is added;
         proper changes are returned.
    PROVIDED all required data is present
    """
    route = urls["create_customer"]

    clear_db()
    data = {"name": "Customer", "contactInfo": "Phone number", "additional": "comment"}
    positive_response = requests.request(
        url=route["route"],
        method=route["method"],
        json=data,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {jwt}"},
    )
    negative_response = requests.request(
        url=route["route"],
        method=route["method"],
        json={},
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {jwt}"},
    )

    queried_customer = Customers.query.filter_by(
        name=data["name"],
        contactInfo=data["contactInfo"],
        additional=data["additional"],
    ).first()

    assert "customers" in json.loads(positive_response.text)
    assert positive_response.status_code == 200
    assert negative_response.status_code == 406
    assert queried_customer


def test_edit_customer(urls, app_client, jwt):
    """
    GIVEN db with a customer instance
    WHEN calling edit customer endpoint
    THEN customer is edited;
         proper changes are returned.
    PROVIDED all required data is present
    """
    route = urls["edit_customer"]

    clear_db()
    customer_data = add_testing_customers()[0]
    data = {
        "id": customer_data["id"],
        "name": "Customer",
        "contactInfo": "phone number1",
        "additional": "comment1",
    }
    positive_response = requests.request(
        url=route["route"],
        method=route["method"],
        json=data,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {jwt}"},
    )
    negative_response = requests.request(
        url=route["route"],
        method=route["method"],
        json={},
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {jwt}"},
    )

    queried_customer = Customers.query.filter_by(
        id=data["id"],
        name=data["name"],
        contactInfo=data["contactInfo"],
        additional=data["additional"],
    ).first()

    assert "customers" in json.loads(positive_response.text)
    assert positive_response.status_code == 200
    assert negative_response.status_code == 406
    assert queried_customer


def test_del_customer(urls, app_client, jwt):
    """
    GIVEN db with a customer instance
    WHEN calling delete customer endpoint
    THEN customer is deleted
    """
    route = urls["del_customer"]

    clear_db()
    customer_data = add_testing_customers()[0]
    response = requests.request(
        url=route["route"] + str(customer_data["id"]),
        method=route["method"],
        headers={"Authorization": f"Bearer {jwt}"},
    )
    queried_customer = Customers.query.filter_by(id=customer_data["id"]).first()

    assert response.status_code == 200
    assert not queried_customer
