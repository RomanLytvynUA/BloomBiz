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


def test_create_product(urls, app_client):
    """
    GIVEN db with category instance
    WHEN calling create product endpoint
    THEN proper product is created
    PROVIDED required data is present.
    """
    url = urls["create_product"]

    clear_db()
    category = add_testing_categories()

    positive_response = requests.post(url=url, json={"product": "Product1", "category": category['name']}, headers={"Content-Type": "application/json"})
    negative_response = requests.post(url=url, json={}, headers={"Content-Type": "application/json"})

    created_product = Goods.query.filter_by(name="Product1", category=Categories.query.filter_by(id=category['id']).first()).all()

    assert positive_response.status_code == 201
    assert negative_response.status_code == 406
    assert len(created_product) == 1


def test_edit_product(urls, app_client):
    """
    GIVEN db with category and goods instances
    WHEN calling edit product endpoint
    THEN proper product is edited
    PROVIDED required data is present,
             id is valid
    """
    url = urls["edit_product"]

    clear_db()
    add_testing_categories()
    product = add_testing_goods(return_obj_dict=True)[0]

    positive_response = requests.put(url=url, json={"product_id": product['id'], "name": "New Name"}, headers={"Content-Type": "application/json"})
    negative_response1 = requests.put(url=url, json={"product_id": 55555, "name": "New Name2"}, headers={"Content-Type": "application/json"})
    negative_response2 = requests.put(url=url, json={}, headers={"Content-Type": "application/json"})

    edited_product = Goods.query.filter_by(id=product['id']).first()

    assert positive_response.status_code == 201
    assert negative_response1.status_code == 406
    assert negative_response2.status_code == 406
    assert edited_product.name == "New Name"


def test_del_product(urls, app_client):
    """
    GIVEN db with category and goods instances
    WHEN calling delete product endpoint
    THEN product is deleted
    PROVIDED id is valid
    """
    url = urls["del_product"]

    clear_db()
    add_testing_categories()
    product = add_testing_goods(return_obj_dict=True)[0]

    positive_response = requests.delete(url=f"{url}/{product['id']}")
    negative_response = requests.delete(url=f"{url}/55555")

    found_products = Goods.query.filter_by(id=product['id']).all()

    assert positive_response.status_code == 200
    assert negative_response.status_code == 406
    assert len(found_products) == 0


def test_create_category(urls, app_client):
    """
    WHEN calling create category endpoint
    THEN proper category is created
    PROVIDED required data is present.
    """
    url = urls["create_category"]

    clear_db()

    positive_response = requests.post(url=url, json={"category": "Category1", "categoryUnits": "units"}, headers={"Content-Type": "application/json"})
    negative_response = requests.post(url=url, json={}, headers={"Content-Type": "application/json"})

    created_category = Categories.query.filter_by(name="Category1", units="units").all()

    assert positive_response.status_code == 201
    assert negative_response.status_code == 406
    assert len(created_category) == 1


def test_edit_category(urls, app_client):
    """
    GIVEN db with category instance
    WHEN calling edit category endpoint
    THEN proper category is edited
    PROVIDED required data is present,
             category name is valid
    """
    url = urls["edit_category"]

    clear_db()
    category = add_testing_categories()

    positive_response = requests.put(url=url, json={"targetCategory": category['name'], "categoryUnits": "New Units", "category": "New Name"}, headers={"Content-Type": "application/json"})
    negative_response1 = requests.put(url=url, json={"targetCategory": "InvalidName", "categoryUnits": "New Units", "category": "New Name"}, headers={"Content-Type": "application/json"})
    negative_response2 = requests.put(url=url, json={}, headers={"Content-Type": "application/json"})

    edited_category = Categories.query.filter_by(id=category['id']).first()

    assert positive_response.status_code == 201
    assert negative_response1.status_code == 406
    assert negative_response2.status_code == 406
    assert edited_category.name == "New Name"
    assert edited_category.units == "New Units"


def test_del_category(urls, app_client):
    """
    GIVEN db with category instance
    WHEN calling delete category endpoint
    THEN category is deleted
    PROVIDED id is valid
    """
    url = urls["del_category"]

    clear_db()
    category = add_testing_categories()

    positive_response = requests.delete(url=f"{url}/{category['id']}")
    negative_response = requests.delete(url=f"{url}/55555")

    found_category = Categories.query.filter_by(id=category['id']).all()

    assert positive_response.status_code == 200
    assert negative_response.status_code == 406
    assert len(found_category) == 0


def test_edit_goods_price(urls, app_client):
    """
    GIVEN db with category and goods instances
    WHEN calling edit goods price endpoint
    THEN product is edited
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
