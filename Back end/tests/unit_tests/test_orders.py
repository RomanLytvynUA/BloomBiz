from src import db
import datetime
from src.models.orders import Orders, OrdersElements
from src.models.suppliers import Suppliers
from src.models.goods import Categories, Goods
from src.utils.orders import util_create_order


def test_orders_elements_generate_dict(app_client):
    """
    GIVEN order & orders element instance
    WHEN calling generate_dict() method on element
    THEN it returns dict with proper data
    """

    category = Categories(name="Test category", units="Test units")
    db.session.add(category)
    db.session.commit()

    product = Goods(name="Test product1", category=category)
    db.session.add(product)
    db.session.commit()

    order = Orders(date="2023-11-01", price=1, status='status', discount=0)
    db.session.add(order)
    db.session.commit()

    element = OrdersElements(quantity=2, price=3, order=order, product=product)
    db.session.add(element)
    db.session.commit()

    assert element.generate_dict() == {'id': element.id,
                                       'quantity': 2,
                                       'price': 3,
                                       'product': product.id,
                                       'order': order.id,
                                       }


def test_orders_generate_dict(app_client):
    """
    GIVEN expense & expenses element instance
    WHEN calling generate_dict() method on expense
    THEN it returns dict with proper data
    """

    category = Categories(name="Test category", units="Test units")
    db.session.add(category)
    db.session.commit()

    product = Goods(name="Test product1", category=category)
    db.session.add(product)
    db.session.commit()

    order = Orders(date="2023-11-01", price=1, status='status', discount=0)
    db.session.add(order)
    db.session.commit()

    element = OrdersElements(quantity=2, price=3, order=order, product=product)
    db.session.add(element)
    db.session.commit()

    assert order.generate_dict() == {'id': order.id,
                                     'date': datetime.date(2023, 11, 1).strftime('%a, %d %b %Y %H:%M:%S GMT'),
                                     'price': 1.0,
                                     'status': 'status',
                                     'discount': 0.0,
                                     'elements': {
                                         "Test category": [{'id': element.id,
                                                            'quantity': 2.0,
                                                            'price': 3.0,
                                                            'product': product.id,
                                                            'order': order.id,
                                                            }]
                                     },
                                     }


def test_util_create_order(app_client):
    """
    GIVEN create order util
    WHEN calling util_create_order()
    THEN it returns proper expense object
    """

    order = util_create_order("2023-11-01", 1, 2, "Status")['order']
    found_order = Orders.query.filter_by(date=datetime.datetime.strptime("2023-11-01", '%Y-%m-%d').date(),
                                         discount=1, price=2, status="Status").all()

    assert len(found_order) == 1
