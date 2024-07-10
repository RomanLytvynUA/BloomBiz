from src import db
from src.models.customers import Customers
from testing_data import clear_db, add_testing_customers, add_testing_orders
from src.utils.customers import util_create_customer, util_edit_customer


def test_customers_generate_dict(app_client):
    """
    GIVEN db with customer and order instances
    WHEN calling generate_dict() method of a customer
    THEN proper data is returned.
    """
    clear_db()
    customer_data = add_testing_customers()[0]
    order_data = add_testing_orders(customer_data["id"])[0]
    customer_data["addresses"] = [order_data["customer_address"]]

    customer_obj = Customers.query.filter_by(id=customer_data["id"]).first()

    assert customer_obj.generate_dict() == customer_data


def test_util_create_customer(app_client):
    """
    GIVEN create customer util
    WHEN calling create customer util with unique contact info
    THEN db contains proper instance of customer;
         output contains proper customer object;
         output contains changes_applied set to true.
    """
    clear_db()

    output = util_create_customer("Name", "Contacts", "Additional")
    queried_customer = Customers.query.filter_by(id=1).first()

    assert queried_customer.name == "Name"
    assert queried_customer.contactInfo == "Contacts"
    assert queried_customer.additional == "Additional"
    assert output["customer"] == queried_customer
    assert output["changes_applied"] == True


def test_util_create_customer_clone(app_client):
    """
    GIVEN db with a customer instance
    WHEN calling create customer util with an existing contact info
    THEN new customer is not added to the db;
         output contains existing customer object;
         output contains changes_applied set to false.
    """
    clear_db()

    customer_data = Customers.query.filter_by(
        id=add_testing_customers()[0]["id"]
    ).first()

    output = util_create_customer("Name1", customer_data.contactInfo, "Additional1")
    queried_customers = Customers.query.filter_by(
        contactInfo=customer_data.contactInfo
    ).all()

    assert len(queried_customers) == 1
    assert output["customer"] == queried_customers[0]


def test_util_edit_customer(app_client):
    """
    GIVEN db with a customer instance
    WHEN calling edit customer util with an existing contact info
    THEN instance of the customer is changed properly;
         output contains proper customer object;
         output contains changes_applied set to true.
    """
    clear_db()
    customer_data = add_testing_customers()[0]

    output = util_edit_customer(
        customer_data["id"], "Name1", "Contacts1", "Additional1"
    )
    queried_customer = Customers.query.filter_by(
        id=customer_data["id"],
        name="Name1",
        contactInfo="Contacts1",
        additional="Additional1",
    ).first()

    assert queried_customer
    assert output["customer"] == queried_customer
    assert output["changes_applied"] == True


def test_util_edit_customer_invalid_id(app_client):
    """
    GIVEN the edit customer util
    WHEN calling edit customer util with an invalid id
    THEN output contains None as customer;
         output contains changes_applied set to false.
    """
    clear_db()

    output = util_edit_customer(55555, "Name1", "Contacts1", "Additional1")

    assert output["customer"] == None
    assert output["changes_applied"] == False
