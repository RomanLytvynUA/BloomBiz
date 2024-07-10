from src import db
from src.models.goods import Categories, Goods
from src.utils.goods import *
from src.utils.settings import util_reset_settings, default_settings
from tests.testing_data import (
    add_testing_orders,
    add_testing_orders_elements,
    add_testing_category,
    add_testing_goods,
    add_testing_expenses,
    add_testing_expenses_elements,
    add_testing_suppliers,
    add_testing_decommissions,
    add_testing_customers,
    clear_db,
)


def test_category_generate_dict(app_client):
    """
    GIVEN category instance with related goods
    WHEN calling generate_dict() method
    THEN dict with proper data is returned
    """
    clear_db()
    category_data = add_testing_category()
    goods_data = add_testing_goods(return_obj_dict=True)

    category_obj = Categories.query.filter_by(id=category_data["id"]).first()

    assert category_obj.generate_dict() == {
        "id": category_data["id"],
        "name": category_data["name"],
        "units": category_data["units"],
        "goods": goods_data,
    }


def test_goods_generate_dict(app_client):
    """
    GIVEN goods instance
    WHEN calling generate_dict() method
    THEN dict with proper data is returned
    """
    clear_db()
    add_testing_category()
    product_name = add_testing_goods()[0]

    product_obj = Goods.query.filter_by(name=product_name).first()

    product_data = product_obj.generate_dict()

    assert "price" in product_data.keys()
    assert "quantity" in product_data.keys()

    # not checking price & qty values, hadnled by util_calc_instock() test
    del product_data["price"]
    del product_data["quantity"]

    assert product_data == {
        "id": product_obj.id,
        "name": product_obj.name,
        "category": product_obj.category_id,
    }


def test_util_create_category(app_client):
    """
    GIVEN create category util
    WHEN calling create category util
    THEN proper category is created;
         output contains proper category instance;
         output contains changes_applied set to true.
    """
    clear_db()
    output = util_create_category("Test category", "Test units")
    queried_category = Categories.query.filter_by(
        name="Test category", units="Test units"
    ).first()

    assert queried_category
    assert output["category"] == queried_category
    assert output["changes_applied"] == True


def test_util_create_category_clone(app_client):
    """
    GIVEN category instance
    WHEN calling create category util with an exicting category name
    THEN dublicated category is not created;
         output contains existing category instance;
         output contains changes_applied set to false.
    """
    clear_db()
    category_data = add_testing_category()

    output = util_create_category(category_data["name"], category_data["units"])
    queried_categories = Categories.query.filter_by(name=category_data["name"]).all()

    assert len(queried_categories) == 1
    assert output["category"] == queried_categories[0]
    assert output["changes_applied"] == False


def test_util_create_product(app_client):
    """
    GIVEN category instance
    WHEN calling create product util
    THEN proper product is created;
         output contains proper product instance;
         output contains changes_applied set to true.
    """
    clear_db()
    category_data = add_testing_category()
    category_obj = Categories.query.filter_by(id=category_data["id"]).first()

    output = util_create_product("Test product", category_obj)
    queried_product = Goods.query.filter_by(
        name="Test product", category=category_obj
    ).first()

    assert queried_product
    assert output["product"] == queried_product
    assert output["changes_applied"] == True


def test_util_create_product_clone(app_client):
    """
    GIVEN category and product instances
    WHEN calling create product util with an exicting product name
    THEN dublicated product is not created;
         output contains existing product instance;
         output contains changes_applied set to false.
    """
    clear_db()
    category_data = add_testing_category()
    existing_product_name = add_testing_goods()[0]
    category_obj = Categories.query.filter_by(id=category_data["id"]).first()

    output = util_create_product(existing_product_name, category_obj)
    queried_products = Goods.query.filter_by(name=existing_product_name).all()

    assert len(queried_products) == 1
    assert output["product"] == queried_products[0]
    assert output["changes_applied"] == False


def test_util_create_decommission(app_client):
    """
    GIVEN category, goods instances
    WHEN calling create decommission util
    THEN decommission is created and returned.
    """
    clear_db()
    add_testing_category()
    product_obj = Goods.query.filter_by(name=add_testing_goods()[0]).first()

    output = util_create_decommission(
        date="2023/11/01",
        product=product_obj,
        quantity=1,
    )
    queried_decommission = Decommissions.query.filter_by(
        id=1,
        date="2023/11/01",
        product=product_obj,
        quantity=1,
    ).first()

    assert queried_decommission
    assert output["decommission"] == queried_decommission


def test_util_set_product_price(app_client):
    """
    GIVEN category, goods instances
    WHEN calling the set product price util
    THEN price is either set to provided or set to None;
         output contains changes_applied set to true.
    """
    clear_db()
    add_testing_category()
    products_data = add_testing_goods(return_obj_dict=True)

    output1 = util_set_product_price(products_data[0]["id"], 1)
    output2 = util_set_product_price(products_data[1]["id"], "RESET")

    product1_price = Goods.query.filter_by(id=1).first().price
    product2_price = Goods.query.filter_by(id=2).first().price

    assert product1_price == 1
    assert product2_price is None
    assert output1["changes_applied"] == True
    assert output2["changes_applied"] == True


def test_util_set_product_price_invalid_id(app_client):
    """
    GIVEN set product price util
    WHEN calling the util with an invalid id
    THEN output contains changes_applied set to false.
    """
    clear_db()

    output = util_set_product_price(55555, 1)

    assert output["changes_applied"] == False


def test_util_calc_instock(app_client):
    """
    GIVEN category, goods, expenses, orders, decommissions elements instances
    WHEN calling util_calc_instock with a product id
    THEN properly calculated data is returned.
    """
    clear_db()
    util_reset_settings()
    add_testing_suppliers()
    add_testing_category()
    add_testing_goods()
    add_testing_expenses()
    add_testing_orders(add_testing_customers()[0]["id"])
    expense_data = add_testing_expenses_elements()
    orders_data = add_testing_orders_elements()
    decomissions_data = add_testing_decommissions()

    expected_product1_quantity = (
        expense_data["elements"][0]["quantity"]
        - list(orders_data["elements"].values())[0][0]["quantity"]
        - decomissions_data[0]["quantity"]
    )
    expected_product1_price = round(
        expense_data["elements"][0]["price"]
        * (default_settings["defaultMargin"] + 100)
        / 100
    )

    # Check the behavior with custom price
    expected_product2_price = 55555
    product2 = Goods.query.filter_by(id=2).first()
    product2.price = expected_product2_price
    db.session.add(product2)
    db.session.commit()
    expected_product2_quantity = (
        expense_data["elements"][1]["quantity"]
        - list(orders_data["elements"].values())[0][1]["quantity"]
    )

    product1_calculations = util_calc_instock(1)
    product2_calculations = util_calc_instock(2)

    assert product1_calculations == {
        "price": expected_product1_price,
        "quantity": expected_product1_quantity,
    }
    assert product2_calculations == {
        "price": expected_product2_price,
        "quantity": expected_product2_quantity,
    }


def test_util_calc_instock_invalid_id(app_client):
    """
    GIVEN the calc instock util
    WHEN calling the util with an invalid id
    THEN placeholder values are returned.
    """
    clear_db()

    output = util_calc_instock(55555)

    assert output == {"price": 0, "quantity": 0}
