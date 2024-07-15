import datetime
import json
import requests
from tests.testing_data import (
    clear_db,
    add_testing_category,
    add_testing_goods,
    add_testing_decommissions,
)
from src.models.goods import Decommissions, Categories, Goods


def test_get_goods(urls, app_client, jwt):
    """
    GIVEN db with category and goods instances
    WHEN calling get goods endpoint
    THEN proper data is returned
    """
    route = urls["get_goods"]

    clear_db()
    category = add_testing_category()
    goods = add_testing_goods(return_obj_dict=True)

    response = requests.request(
        url=route["route"],
        method=route["method"],
        headers={"Authorization": f"Bearer {jwt}"},
    )

    assert json.loads(response.text) == [
        {
            "goods": [product for product in goods],
            "id": category["id"],
            "name": category["name"],
            "units": category["units"],
        }
    ]


def test_create_product(urls, app_client, jwt):
    """
    GIVEN db with category instance
    WHEN calling create product endpoint
    THEN proper product is created;
         proper changes are returned.
    PROVIDED required data is present.
    """
    route = urls["create_product"]

    clear_db()
    category = add_testing_category()

    positive_response = requests.request(
        url=route["route"],
        method=route["method"],
        json={"product": "Product1", "category": category["name"]},
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {jwt}"},
    )
    negative_response = requests.request(
        url=route["route"],
        method=route["method"],
        json={},
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {jwt}"},
    )

    created_product = Goods.query.filter_by(
        name="Product1", category=Categories.query.filter_by(id=category["id"]).first()
    ).all()

    assert "goods" in json.loads(positive_response.text)
    assert positive_response.status_code == 201
    assert negative_response.status_code == 406
    assert len(created_product) == 1


def test_edit_product(urls, app_client, jwt):
    """
    GIVEN db with category and goods instances
    WHEN calling edit product endpoint
    THEN proper product is edited;
         proper changes are returned.
    PROVIDED required data is present;
             id is valid.
    """
    route = urls["edit_product"]

    clear_db()
    add_testing_category()
    product = add_testing_goods(return_obj_dict=True)[0]

    positive_response = requests.request(
        url=route["route"],
        method=route["method"],
        json={"product_id": product["id"], "name": "New Name"},
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {jwt}"},
    )
    negative_response1 = requests.request(
        url=route["route"],
        method=route["method"],
        json={"product_id": 55555, "name": "New Name2"},
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {jwt}"},
    )
    negative_response2 = requests.request(
        url=route["route"],
        method=route["method"],
        json={},
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {jwt}"},
    )

    edited_product = Goods.query.filter_by(id=product["id"]).first()

    assert "goods" in json.loads(positive_response.text)
    assert positive_response.status_code == 201
    assert negative_response1.status_code == 406
    assert negative_response2.status_code == 406
    assert edited_product.name == "New Name"


def test_del_product(urls, app_client, jwt):
    """
    GIVEN db with category and goods instances
    WHEN calling delete product endpoint
    THEN product is deleted
    PROVIDED id is valid
    """
    route = urls["del_product"]

    clear_db()
    add_testing_category()
    product = add_testing_goods(return_obj_dict=True)[0]

    positive_response = requests.request(
        url=f"{route['route']}/{product['id']}",
        method=route["method"],
        headers={"Authorization": f"Bearer {jwt}"},
    )
    negative_response = requests.request(
        url=f"{route['route']}/55555",
        method=route["method"],
        headers={"Authorization": f"Bearer {jwt}"},
    )

    queried_products = Goods.query.filter_by(id=product["id"]).first()

    assert positive_response.status_code == 200
    assert negative_response.status_code == 406
    assert not queried_products


def test_create_category(urls, app_client, jwt):
    """
    WHEN calling create category endpoint
    THEN proper category is created;
         proper changes are returned.
    PROVIDED required data is present.
    """
    route = urls["create_category"]

    clear_db()

    positive_response = requests.request(
        url=route["route"],
        method=route["method"],
        json={"category": "Category1", "categoryUnits": "units"},
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {jwt}"},
    )
    negative_response = requests.request(
        url=route["route"],
        method=route["method"],
        json={},
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {jwt}"},
    )

    created_category = Categories.query.filter_by(name="Category1", units="units").all()

    assert "categories" in json.loads(positive_response.text)
    assert positive_response.status_code == 201
    assert negative_response.status_code == 406
    assert len(created_category) == 1


def test_edit_category(urls, app_client, jwt):
    """
    GIVEN db with category instance
    WHEN calling edit category endpoint
    THEN proper category is edited;
         proper changes are returned.
    PROVIDED required data is present,
             category name is valid
    """
    route = urls["edit_category"]

    clear_db()
    category = add_testing_category()

    positive_response = requests.request(
        url=route["route"],
        method=route["method"],
        json={
            "targetCategory": category["name"],
            "categoryUnits": "New Units",
            "category": "New Name",
        },
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {jwt}"},
    )
    negative_response1 = requests.request(
        url=route["route"],
        method=route["method"],
        json={
            "targetCategory": "InvalidName",
            "categoryUnits": "New Units",
            "category": "New Name",
        },
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {jwt}"},
    )
    negative_response2 = requests.request(
        url=route["route"],
        method=route["method"],
        json={},
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {jwt}"},
    )

    edited_category = Categories.query.filter_by(id=category["id"]).first()

    assert "categories" in json.loads(positive_response.text)
    assert positive_response.status_code == 201
    assert negative_response1.status_code == 406
    assert negative_response2.status_code == 406
    assert edited_category.name == "New Name"
    assert edited_category.units == "New Units"


def test_del_category(urls, app_client, jwt):
    """
    GIVEN db with category instance
    WHEN calling delete category endpoint
    THEN category is deleted.
    PROVIDED id is valid
    """
    route = urls["del_category"]

    clear_db()
    category = add_testing_category()

    positive_response = requests.request(
        url=f"{route['route']}/{category['id']}",
        method=route["method"],
        headers={"Authorization": f"Bearer {jwt}"},
    )
    negative_response = requests.request(
        url=f"{route['route']}/55555",
        method=route["method"],
        headers={"Authorization": f"Bearer {jwt}"},
    )

    found_category = Categories.query.filter_by(id=category["id"]).all()

    assert positive_response.status_code == 200
    assert negative_response.status_code == 406
    assert len(found_category) == 0


def test_edit_goods_price(urls, app_client, jwt):
    """
    GIVEN db with category and goods instances
    WHEN calling edit goods price endpoint
    THEN product is edited;
         proper changes are returned.
    PROVIDED that required data is present
    """
    route = urls["edit_goods_price"]

    clear_db()
    add_testing_category()
    add_testing_goods()

    data1 = {"product_id": 1, "price": 55555}
    data2 = {"product_id": 2, "price": "RESET"}
    positive_response1 = requests.request(
        url=route["route"],
        method=route["method"],
        json=data1,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {jwt}"},
    )
    positive_response2 = requests.request(
        url=route["route"],
        method=route["method"],
        json=data2,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {jwt}"},
    )
    negative_response = requests.request(
        url=route["route"],
        method=route["method"],
        json={},
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {jwt}"},
    )

    queried_price1 = Goods.query.filter_by(id=1).first().price
    queried_price2 = Goods.query.filter_by(id=2).first().price

    assert "goods" in json.loads(positive_response1.text)
    assert "goods" in json.loads(positive_response2.text)
    assert negative_response.status_code == 406
    assert positive_response1.status_code == 200
    assert positive_response2.status_code == 200
    assert queried_price1 == 55555
    assert queried_price2 is None


def test_create_decommission(urls, app_client, jwt):
    """
    GIVEN db with category and goods instances
    WHEN calling create decommission endpoint
    THEN proper data is returned;
         proper changes are returned.
    PROVIDED required data is present.
    """
    route = urls["create_decommission"]

    clear_db()
    add_testing_category()
    product = add_testing_goods()[0]
    product_obj = Goods.query.filter_by(name=product).first()

    data = {
        "date": "2023/11/1",
        "quantity": 1,
        "productId": product_obj.id,
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

    queried_decommission = Decommissions.query.filter_by(
        date=data["date"], quantity=data["quantity"], product_id=data["productId"]
    ).first()

    assert positive_response.status_code == 200
    assert negative_response.status_code == 406
    assert "goods" in json.loads(positive_response.text)
    assert queried_decommission


def test_del_decommission(urls, app_client, jwt):
    """
    GIVEN db with a decommission instance
    WHEN calling delete decommission endpoint
    THEN decommission is deleted
    """
    route = urls["del_decommission"]

    clear_db()
    add_testing_category()
    add_testing_goods()
    decommission = add_testing_decommissions()[0]

    response = requests.request(
        url=route["route"] + str(decommission["id"]),
        method=route["method"],
        headers={"Authorization": f"Bearer {jwt}"},
    )
    queried_decommission = Decommissions.query.filter_by(id=decommission["id"]).first()

    assert response.status_code == 200
    assert not queried_decommission


def test_get_decommission(urls, jwt):
    """
    GIVEN db with decommission instance
    WHEN calling get decommissions endpoint
    THEN proper data is returned
    """
    route = urls["get_decommissions"]

    clear_db()
    add_testing_category()
    add_testing_goods()
    decommissions = add_testing_decommissions()

    response = requests.request(
        url=route["route"],
        method=route["method"],
        headers={"Authorization": f"Bearer {jwt}"},
    )

    assert response.status_code == 200
    assert json.loads(response.text) == decommissions
