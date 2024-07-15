import json
import requests
from src.models.goods import Goods
from src.models.orders import Orders, OrdersElements
from tests.testing_data import (
    clear_db,
    add_testing_orders,
    add_testing_category,
    add_testing_goods,
    add_testing_orders_elements,
    add_testing_customers,
)


def test_get_orders(urls, jwt):
    """
    GIVEN db with categories, goods, orders instances
    WHEN calling get orders endpoint
    THEN proper data is returned
    """
    route = urls["get_orders"]

    clear_db()
    add_testing_category()
    add_testing_goods()
    add_testing_orders(add_testing_customers()[0]["id"])
    order = add_testing_orders_elements()

    response = requests.get(
        url=route["route"], headers={"Authorization": f"Bearer {jwt}"}
    )

    assert json.loads(response.text) == [order]


def test_create_order(urls, app_client, jwt):
    """
    GIVEN category, goods instances
    WHEN calling create order endpoint
    THEN new order is added;
         proper changes are returned.
    PROVIDED all required data is present
    """
    route = urls["create_order"]

    clear_db()
    category = add_testing_category()["name"]
    products = add_testing_goods()
    data = {
        "date": "2023/11/1",
        "price": 1,
        "status": "Status",
        "additional": "Additional",
        "discount": 2,
        "elements": {
            category: [
                {"product": products[0], "quantity": 2, "price": 3},
                {"product": products[1], "quantity": 4, "price": 5},
            ]
        },
    }

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

    queried_order = Orders.query.filter_by(
        date=data["date"],
        price=data["price"],
        discount=data["discount"],
        status=data["status"],
        additional=data["additional"],
    ).first()
    order_elements = OrdersElements.query.filter_by(order=queried_order).all()

    assert not len(
        {"orders", "goods", "customers"}
        - set(json.loads(positive_response.text).keys())
    )
    assert positive_response.status_code == 200
    assert negative_response.status_code == 406
    assert queried_order
    assert len(order_elements) == 2
    assert order_elements[0].generate_dict() == {
        "id": 1,
        "quantity": 2.0,
        "price": 3.0,
        "product": 1,
        "order": queried_order.id,
    }
    assert order_elements[1].generate_dict() == {
        "id": 2,
        "quantity": 4.0,
        "price": 5.0,
        "product": 2,
        "order": queried_order.id,
    }


def test_edit_order(urls, app_client, jwt):
    """
    GIVEN db with an order instance
    WHEN calling edit order endpoint
    THEN order is edited;
         proper changes are returned.
    PROVIDED all required data is present
    """
    route = urls["edit_order"]

    clear_db()
    category = add_testing_category()["name"]
    products = add_testing_goods()
    add_testing_orders(add_testing_customers()[0]["id"])
    order_data = add_testing_orders_elements()
    data = {
        "order_id": order_data["id"],
        "date": "2011/11/11",
        "price": 4444,
        "status": "NewStatus",
        "discount": 55555,
        "additional": "NewAdditional",
        "elements": {
            category: [
                {"product": products[0], "quantity": 333, "price": 4444},
            ]
        },
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

    queried_order = Orders.query.filter_by(
        id=order_data["id"],
        price=data["price"],
        date=data["date"],
        status=data["status"],
        additional=data["additional"],
        discount=data["discount"],
    ).first()
    order_element = OrdersElements.query.filter_by(
        order=queried_order,
        quantity=333,
        price=4444,
        product=Goods.query.filter_by(name=products[0]).first(),
    ).first()

    assert positive_response.status_code == 200
    assert negative_response.status_code == 406
    assert queried_order
    assert order_element


def test_del_order(urls, app_client, jwt):
    """
    GIVEN db with an order instance
    WHEN calling delete order endpoint
    THEN order is deleted
    """
    route = urls["del_order"]

    clear_db()
    add_testing_category()
    add_testing_goods()
    add_testing_orders(add_testing_customers()[0]["id"])
    order_data = add_testing_orders_elements()
    response = requests.delete(
        url=route["route"] + str(order_data["id"]),
        headers={"Authorization": f"Bearer {jwt}"},
    )
    order = Orders.query.filter_by(id=order_data["id"]).all()

    assert response.status_code == 200
    assert not len(order)
