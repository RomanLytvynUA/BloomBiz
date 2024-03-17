import datetime
import json
import requests
from tests.testing_data import clear_db, add_testing_categories, add_testing_goods, add_testing_decommissions
from src.models.goods import Decommissions, Categories, Goods


def test_get_goods(urls, app_client):
    """
    GIVEN db with category and goods instances
    WHEN calling get goods endpoint
    THEN proper data is returned
    """
    url = urls["get_goods"]

    clear_db()
    category = add_testing_categories()
    goods = add_testing_goods(return_obj_dict=True)

    response = requests.get(url=url)

    assert json.loads(response.text) == [{"goods": [product for product in goods], "id": category['id'],
                                          "name": category['name'], "units": category['units']}]


def test_edit_goods_price(urls, app_client):
    """
    GIVEN db with category and goods instances
    WHEN calling edit goods price endpoint
    THEN product price is edited
         provided that required data is present
    """
    url = urls["edit_goods_price"]

    clear_db()
    add_testing_categories()
    add_testing_goods()

    data1 = {'product_id': 1, 'price': 55555}
    data2 = {'product_id': 2, 'price': "RESET"}
    positive_response1 = requests.post(url=url, json=data1, headers={"Content-Type": "application/json"})
    positive_response2 = requests.post(url=url, json=data2, headers={"Content-Type": "application/json"})
    negative_response = requests.post(url=url, json={}, headers={"Content-Type": "application/json"})

    queried_price1 = Goods.query.filter_by(id=1).first().price
    queried_price2 = Goods.query.filter_by(id=2).first().price

    assert negative_response.status_code == 406
    assert positive_response1.status_code == 200
    assert positive_response2.status_code == 200
    assert queried_price1 == 55555
    assert queried_price2 is None


def test_create_decommission(urls, app_client):
    """
    GIVEN db with category and goods instances
    WHEN calling create decommission endpoint
    THEN proper data is returned
    PROVIDED required data is present.
    """
    url = urls["create_decommission"]

    clear_db()
    category = add_testing_categories()['name']
    product = add_testing_goods()[0]
    product_obj = Goods.query.filter_by(name=product).first()

    data = {'date': "2023/11/1", 'quantity': 1, 'category': category, 'product': product}

    positive_response = requests.post(url=url, json=data, headers={"Content-Type": "application/json"})
    negative_response = requests.post(url=url, json={}, headers={"Content-Type": "application/json"})

    found_decommission = Decommissions.query.filter_by(date="2023/11/1", quantity=1, product=product_obj).all()

    assert positive_response.status_code == 200
    assert negative_response.status_code == 406
    assert len(found_decommission)


def test_del_decommission(urls, app_client):
    """
    GIVEN db with a decommission instance
    WHEN calling delete supplier endpoint
    THEN supplier is deleted
    """
    url = urls["del_decommission"]

    clear_db()
    add_testing_categories()
    add_testing_goods()
    decommission = add_testing_decommissions()[0]

    response = requests.delete(url=url+str(decommission['id']))
    supplier = Decommissions.query.filter_by(id=decommission['id']).all()

    assert response.status_code == 200
    assert not len(supplier)


def test_get_decommission(urls):
    """
    GIVEN db with decommission instance
    WHEN calling get decommissions endpoint
    THEN proper data is returned
    """
    url = urls["get_decommissions"]

    clear_db()
    add_testing_categories()
    add_testing_goods()
    decommission = add_testing_decommissions()

    response = requests.get(url=url)

    assert response.status_code == 200
    assert json.loads(response.text) == decommission
