from src import db
from src.models.customers import Customers
from testing_data import clear_db, add_testing_customers
from src.utils.customers import util_create_customer


def test_util_create_customer(app_client):
    """
    GIVEN create customer util
    WHEN calling create customer util with unique address
    THEN db contains proper instance of customer;
         proper instance of customer is returned;
    """
    clear_db()
    customer = util_create_customer("Name", "Contacts", "Address", "-")['customer']

    queried_customer = Customers.query.filter_by(id=1).first()

    assert queried_customer.name == "Name"
    assert queried_customer.contactInfo == "Contacts"
    assert queried_customer.address == "Address"
    assert queried_customer.additional == "-"


def test_util_create_customer_clone(app_client):
    """
    GIVEN db with a customer instance
    WHEN calling create customer util with an existing contact info
    THEN new customer is not added to the db;
         proper instance of customer is returned;
    """
    clear_db()
    customer_data = Customers.query.filter_by(id=add_testing_customers()[0]['id']).first()

    customer_obj = util_create_customer("Name1", customer_data.contactInfo, "Address1", "-1")['customer']

    queried_customers = Customers.query.filter_by(contactInfo=customer_data.contactInfo).all()

    assert len(queried_customers) == 1
    assert customer_obj == customer_data
    assert queried_customers[0].name == customer_data.name
    assert queried_customers[0].contactInfo == customer_data.contactInfo
    assert queried_customers[0].address == customer_data.address
    assert queried_customers[0].additional == customer_data.additional

