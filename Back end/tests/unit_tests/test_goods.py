from src import db
from src.models.goods import Categories, Goods
from src.utils.goods import *
from src.utils.settings import util_reset_settings, default_settings
from tests.testing_data import add_testing_orders, add_testing_orders_elements, \
    add_testing_categories, add_testing_goods, add_testing_expenses, add_testing_expenses_elements, \
    add_testing_suppliers, add_testing_decommissions, add_testing_customers, clear_db


def test_category_generate_dict(app_client):
    """
    GIVEN category instance with related goods
    WHEN calling generate_dict() method
    THEN dict with proper data is returned 
    """
    clear_db()
    category_data = add_testing_categories()
    goods_data = add_testing_goods(return_obj_dict=True)

    category_obj = Categories.query.filter_by(id=category_data['id']).first()

    assert category_obj.generate_dict() == {'id': category_data['id'],
                                            'name': category_data['name'],
                                            'units': category_data['units'],
                                            'goods': goods_data,
                                            }


def test_util_create_category(app_client):
    """
    GIVEN create category util
    WHEN calling create category util
    THEN proper category is created;
         proper category instance is returned;
    """
    clear_db()
    category = util_create_category("Test category", "Test units")['category']
    queried_category = Categories.query.filter_by(id=1).first()

    assert queried_category
    assert category == queried_category
    assert category.name == "Test category"
    assert category.units == "Test units"


def test_util_create_category_clone(app_client):
    """
    GIVEN category instance
    WHEN calling create category util with an exicting category name
    THEN dublicated category is not created;
         category instance is returned;
    """
    clear_db()
    category_data = add_testing_categories()
    category = util_create_category(category_data['name'], category_data['units'])['category']

    queried_categories = Categories.query.filter_by(name=category_data['name']).all()

    assert len(queried_categories) == 1
    assert category == queried_categories[0]
    assert category.name == category_data['name']
    assert category.units == category_data['units']


def test_util_create_product(app_client):
    """
    GIVEN category instance
    WHEN calling create product util
    THEN proper product is created;
         proper product instance is returned.
    """
    clear_db()
    category_data = add_testing_categories()
    category_obj = Categories.query.filter_by(id=category_data['id']).first()

    product = util_create_product("Test product", category_obj)['product']
    queried_product = Goods.query.filter_by(id=1).first()

    assert queried_product
    assert product == queried_product
    assert product.name == "Test product"
    assert product.category.name == category_data['name']


def test_util_create_product_clone(app_client):
    """
    GIVEN category and product instances
    WHEN calling create product util with exicting product name
    THEN dublicated product is not created;
         proper product instance is returned.
    """
    clear_db()
    category_data = add_testing_categories()
    product_name = add_testing_goods()[0]
    category_obj = Categories.query.filter_by(id=category_data['id']).first()

    product = util_create_product(product_name, category_obj)['product']
    queried_products = Goods.query.filter_by(name=product_name).all()

    assert len(queried_products) == 1
    assert product == queried_products[0]
    assert product.name == product_name
    assert product.category.name == category_data['name']


def test_util_calc_instock(app_client):
    """
    GIVEN category, goods, expenses, orders, decommissions elements instances
    WHEN calling util_calc_instock
    THEN properly calculated data is returned;
    """
    clear_db()
    util_reset_settings()
    add_testing_suppliers()
    add_testing_categories()
    add_testing_goods()
    add_testing_expenses()
    expense_data = add_testing_expenses_elements()
    add_testing_orders(add_testing_customers()[0]['id'])
    orders_data = add_testing_orders_elements()
    decomissions_data = add_testing_decommissions()

    expected_product1_quantity = expense_data['elements'][0]['quantity']-list(orders_data['elements'].values())[0][0]['quantity']-decomissions_data[0]['quantity']
    expected_product1_price = round(expense_data['elements'][0]['price']*(default_settings['defaultMargin']+100)/100)
    
    # Setting product2 price to custom in order to check price selection functionality
    expected_product2_price = 55555
    product2 = Goods.query.filter_by(id=2).first()
    product2.price = expected_product2_price
    db.session.add(product2)
    db.session.commit()
    expected_product2_quantity = expense_data['elements'][1]['quantity']-list(orders_data['elements'].values())[0][1]['quantity']

    calculated_goods = util_calc_instock()

    assert calculated_goods == [{'category': 'Category', 'category_id': 1, 'product': 'Product1',
                                 'quantity': float(expected_product1_quantity), 'id': 1, 'units': 'units', 'price': float(expected_product1_price)},
                                {'category': 'Category', 'product': 'Product2', 'quantity': float(expected_product2_quantity),
                                 'id': 2, 'category_id': 1, 'units': 'units', 'price': float(expected_product2_price)}]


def test_util_create_decommission(app_client):
    """
    GIVEN category, goods instances
    WHEN calling util_create_decommission
    THEN decommission is created and returned.
    """
    clear_db()
    category = add_testing_categories()['name']
    product = add_testing_goods()[0]

    decommission = util_create_decommission(date="2023/11/01", product=product, quantity=1,
                                            category=category)['decommission']
    found_decommission = Decommissions.query.filter_by(id=1, date="2023/11/01", product=Goods.query.filter_by(name=product).first(), 
                                                       quantity=1).first()

    assert decommission == found_decommission


def test_util_create_decommission_invalid_category(app_client):
    """
    GIVEN util_create_decommission
    WHEN calling util_create_decommission with invalid category name
    THEN decommission is NOT created and proper message is returned returned.
    """
    clear_db()

    feedback = util_create_decommission(date="2023/11/01", product='', quantity=1, category='')['message']
    found_decommissions = Decommissions.query.all()

    assert not len(found_decommissions)
    assert feedback == 'Failed to fetch provided category.'


def test_util_set_product_price(app_client):
    """
    GIVEN category, goods, expense instances
    WHEN calling util_set_product_price
    THEN price is either set to provided or set to None.
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
