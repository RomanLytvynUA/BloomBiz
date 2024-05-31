import json
import requests
from src.models.goods import Goods
from src.models.orders import Orders, OrdersElements
from tests.testing_data import clear_db, add_testing_orders, \
    add_testing_categories, add_testing_goods, \
    add_testing_orders_elements, add_testing_customers


def test_get_orders(urls):
    """
    GIVEN db with categories, goods, orders instances
    WHEN calling get orders endpoint
    THEN proper data is returned
    """
    url = urls["get_orders"]

    clear_db()
    add_testing_categories()
    add_testing_goods()
    add_testing_orders(add_testing_customers()[0]['id'])
    order = add_testing_orders_elements()

    response = requests.get(url=url)

    assert json.loads(response.text) == [order]


def test_create_order(urls, app_client):
    """
    GIVEN category, goods instances
    WHEN calling create order endpoint
    THEN new order is added
    PROVIDED all required data is present
    """
    url = urls["create_order"]

    clear_db()
    category = add_testing_categories()['name']
    products = add_testing_goods()
    data = {'date': "2023/11/1", 'price': 1, 'status': 'Status', 'discount': 2, "elements": {
        category: [
            {'product': products[0], 'quantity': 2, 'price': 3},
            {'product': products[1], 'quantity': 3, 'price': 4},
        ]
    }}

    positive_response = requests.post(url=url, json=data, headers={"Content-Type": "application/json"})
    negative_response = requests.post(url=url, json={}, headers={"Content-Type": "application/json"})

    order = Orders.query.filter_by(date=data['date'], price=data['price'], discount=data['discount'],
                                   status=data['status']).all()
    orders_elements = OrdersElements.query.filter_by(order=order[0]).all()

    assert positive_response.status_code == 200
    assert negative_response.status_code == 406
    assert len(order)
    assert len(orders_elements) == 2
    assert orders_elements[0].generate_dict() == {'id': 1,
                                                  'quantity': 2.0,
                                                  'price': 3.0,
                                                  'product': 1,
                                                  'order': order[0].id,
                                                  }


def test_edit_order(urls, app_client):
    """
    GIVEN db with an order instance
    WHEN calling edit order endpoint
    THEN order is edited
    PROVIDED all required data is present
    """
    url = urls["edit_order"]

    clear_db()
    category = add_testing_categories()['name']
    products = add_testing_goods()
    add_testing_orders(add_testing_customers()[0]['id'])
    order_data = add_testing_orders_elements()
    data = {'order_id': order_data['id'], 'date': "2023/11/1", 'price': 1, 'status': 'Status', 'discount': 2,
            "elements": {
                category: [
                    {'product': products[0], 'quantity': 3, 'price': 1},
                ]
            }}

    positive_response = requests.put(url=url, json=data, headers={"Content-Type": "application/json"})
    negative_response = requests.put(url=url, json={}, headers={"Content-Type": "application/json"})

    edited_order = Orders.query.filter_by(id=order_data['id']).all()
    order_elements = OrdersElements.query.filter_by(order=edited_order[0], quantity=3, price=1,
                                                    product=Goods.query.filter_by(name=products[0]).first()).all()

    assert positive_response.status_code == 200
    assert negative_response.status_code == 406
    assert len(edited_order)
    assert len(order_elements) == 1


def test_del_order(urls, app_client):
    """
    GIVEN db with an order instance
    WHEN calling delete order endpoint
    THEN order is deleted
    """
    url = urls["del_order"]

    clear_db()
    add_testing_categories()
    add_testing_goods()
    add_testing_orders(add_testing_customers()[0]['id'])
    order_data = add_testing_orders_elements()
    response = requests.delete(url=url+str(order_data['id']))
    order = Orders.query.filter_by(id=order_data['id']).all()

    assert response.status_code == 200
    assert not len(order)
