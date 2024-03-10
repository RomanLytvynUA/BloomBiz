from src import db
import datetime
from src.models.expenses import Expenses, ExpensesElements
from src.models.suppliers import Suppliers
from src.models.goods import Categories, Goods
from src.utils.expenses import *


def test_expenses_elements_generate_dict(app_client):
    """
    GIVEN expense & expenses element instance
    WHEN calling generate_dict() method on element
    THEN it returns dict with proper data
    """

    category = Categories(name="Test category", units="Test units")
    supplier = Suppliers(name="Test supplier", contactInfo="-", additional='-')
    db.session.add_all([category, supplier])
    db.session.commit()

    product = Goods(name="Test product1", category=category)
    db.session.add(product)
    db.session.commit()

    expense = Expenses(date="2023-11-01", total=1, supplier=supplier, category=category)
    db.session.add(expense)
    db.session.commit()

    element = ExpensesElements(quantity=2, price=3, expense=expense, product=product)
    db.session.add(element)
    db.session.commit()

    assert element.generate_dict() == {'id': element.id,
                                       'quantity': 2,
                                       'price': 3,
                                       'product': product.id,
                                       'expense': expense.id,
                                       }


def test_expense_generate_dict(app_client):
    """
    GIVEN expense & expenses element instance
    WHEN calling generate_dict() method on expense
    THEN it returns dict with proper data
    """

    category = Categories(name="Test category", units="Test units")
    supplier = Suppliers(name="Test supplier", contactInfo="-", additional='-')
    db.session.add_all([category, supplier])
    db.session.commit()

    product = Goods(name="Test product1", category=category)
    db.session.add(product)
    db.session.commit()

    expense = Expenses(date="2023-11-01", total=1, supplier=supplier, category=category)
    db.session.add(expense)
    db.session.commit()

    element = ExpensesElements(quantity=2, price=3, expense=expense, product=product)
    db.session.add(element)
    db.session.commit()

    assert expense.generate_dict() == {'id': expense.id,
                                       'date': datetime.date(2023, 11, 1).strftime('%a, %d %b %Y %H:%M:%S GMT'),
                                       'total': 1,
                                       'supplier': supplier.id,
                                       'category': category.id,
                                       'elements': [
                                           {'id': element.id,
                                            'quantity': 2,
                                            'price': 3,
                                            'product': product.id,
                                            'expense': expense.id,
                                            }
                                       ],
                                       }


def test_util_create_expense(app_client):
    """
    GIVEN create category & supplier utils
    WHEN calling util_create_expense()
    THEN it returns proper expense object
    """

    expense = util_create_expense("2023-11-01", 1, "Test supplier", "Test category", "Test units")['expense']
    found_expense = Expenses.query.filter_by(date=datetime.datetime.strptime("2023-11-01", '%Y-%m-%d').date(),
                                             total=1, supplier=Suppliers.query.filter_by(name="Test supplier").all()[0],
                                             category=Categories.query.filter_by(name="Test category").all()[0]
                                             ).all()

    assert len(found_expense) == 1
