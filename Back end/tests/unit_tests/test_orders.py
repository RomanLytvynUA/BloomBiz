from src import db
import datetime
from src.models.orders import Orders, OrdersElements
from src.models.suppliers import Suppliers
from src.models.goods import Categories, Goods
from src.models.customers import Customers
from src.utils.orders import util_create_order
from testing_data import clear_db, add_testing_orders, add_testing_customers, add_testing_orders_elements, add_testing_categories, add_testing_goods


def test_orders_generate_dict(app_client):
    """
    GIVEN order, orders elements instances
    WHEN calling generate_dict() method on order
    THEN dict with proper data is returned
    """
    clear_db()
    add_testing_categories()
    add_testing_goods()
    order_data = add_testing_orders(add_testing_customers()[0]['id'])[0]
    order_data['elements'] = add_testing_orders_elements(return_raw=True)

    order_data['receiver'] = Customers.query.filter_by(id=order_data['receiver_id']).first().generate_dict()
    del order_data['receiver_id']
    order_data['customer'] = Customers.query.filter_by(id=order_data['customer_id']).first().generate_dict()
    del order_data['customer_id']

    order_obj = Orders.query.filter_by(id=order_data['id']).first()

    assert order_obj.generate_dict() == order_data


def test_util_create_order(app_client):
    """
    GIVEN create order util
    WHEN calling util_create_order()
    THEN proper order object is returned;
         new order is added to the db.
    """

    order = util_create_order("2023-11-01", 1, 2, "Status")['order']
    found_order = Orders.query.filter_by(date=datetime.datetime.strptime("2023-11-01", '%Y-%m-%d').date(),
                                         discount=1, price=2, status="Status").all()

    assert len(found_order) == 1
    assert found_order[0] == order
