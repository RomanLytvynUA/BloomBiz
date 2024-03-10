from src import db
from src.models.goods import Categories, Goods
from src.utils.goods import *
from tests.testing_data import add_testing_orders, add_testing_orders_elements, \
    add_testing_categories, add_testing_goods, add_testing_expenses, add_testing_expenses_elements, \
    add_testing_suppliers, add_testing_decommissions, clear_db


def test_category_generate_dict(app_client):
    """
    GIVEN category instance with related goods
    WHEN calling generate_dict() method
    THEN it should return dict with proper data
    """

    category = Categories(name="Test category", units="Test units")
    db.session.add(category)
    db.session.commit()

    product1 = Goods(name="Test product1", category=category)
    product2 = Goods(name="Test product2", category=category)
    db.session.add_all([product1, product2])
    db.session.commit()

    assert category.generate_dict() == {'id': category.id,
                                        'name': "Test category",
                                        'units': "Test units",
                                        'goods': [{"name": "Test product1", "id": 1, "category": 1},
                                                  {"name": "Test product2", "id": 2, "category": 1}],
                                        }


def test_util_create_category(app_client):
    """
    GIVEN create_category func
    WHEN calling function
    THEN it creates proper category;
         returns category instance;
         doesn't add category if such name already exists.
    """

    new_category = util_create_category("Test category", "Test units")['category']
    duplicated_category = util_create_category("Test category", "Test units")['category']

    categories = list(Categories.query.filter_by(name="Test category").all())

    assert categories[0].name == "Test category"
    assert len(categories) == 1
    assert categories[0] == new_category
    assert categories[0] == duplicated_category


def test_util_create_goods(app_client):
    """
    GIVEN category and goods instance
    WHEN calling function
    THEN it creates proper product;
         returns product instance;
         doesn't create product if such name already exists.
    """

    category = Categories(name="Test category", units="Test units")
    db.session.add(category)
    db.session.commit()

    product1 = Goods(name="Test product1", category=category)
    db.session.add(product1)
    db.session.commit()

    new_product = util_create_product("Test product2", category)['product']
    duplicated_product = util_create_product("Test product1", category)['product']

    goods = list(Goods.query.filter_by(category=category).all())

    assert new_product in goods
    assert len(goods) == 2
    assert duplicated_product == product1


def test_util_calc_instock(app_client):
    """
    GIVEN category and goods, expenses, orders, decommissions elements instances
    WHEN calling util_calc_instock
    THEN proper data is returned;
         no data is returned if quantity is 0.
    """
    clear_db()
    add_testing_suppliers()
    add_testing_categories()
    add_testing_goods()
    add_testing_expenses()
    add_testing_expenses_elements()
    add_testing_orders()
    add_testing_orders_elements()
    add_testing_decommissions()

    calculated_goods = util_calc_instock()

    assert calculated_goods == [{'category': 'Category', 'category_id': 1, 'product': 'Product1',
                                 'quantity': 1, 'id': 1, 'units': 'units', 'price': 5},
                                {'category': 'Category', 'product': 'Product2', 'quantity': 0,
                                 'id': 2, 'category_id': 1, 'units': 'units', 'price': 5}]


def test_util_create_decommission(app_client):
    """
    GIVEN category, goods instances
    WHEN calling util_create_decommission
    THEN decommission is created.
    """
    clear_db()
    category = add_testing_categories()['name']
    product = add_testing_goods()[0]

    decommission = util_create_decommission(date="2023/11/01", product=product, quantity=1,
                                            category=category)['decommission']
    found_decommission = Decommissions.query.filter_by(id=1).first()

    assert decommission == found_decommission


def test_util_set_product_price(app_client):
    """
    GIVEN category, goods, expense instances
    WHEN calling util_set_product_price
    THEN price is either set to provided or changed according to last expense.
    """
    clear_db()
    add_testing_categories()
    products = add_testing_goods(return_obj_dict=True)
    add_testing_suppliers()
    add_testing_expenses()
    add_testing_expenses_elements()

    util_set_product_price(products[0]['id'], 1)
    util_set_product_price(products[1]['id'], "RESET")

    product1_price = Goods.query.filter_by(id=1).first().price
    product2_price = Goods.query.filter_by(id=2).first().price

    assert product1_price == 1
    assert product2_price is None
