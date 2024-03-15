from src import db
import datetime
from src.models.expenses import Expenses, ExpensesElements
from src.models.suppliers import Suppliers
from src.models.goods import Categories, Goods
from src.utils.expenses import *
from testing_data import clear_db, add_testing_expenses, add_testing_expenses_elements, add_testing_categories, add_testing_goods, add_testing_suppliers


def test_expense_generate_dict(app_client):
    """
    GIVEN expense, expenses elements instances
    WHEN calling generate_dict() method on expense
    THEN it returns dict with proper data
    """

    clear_db()
    add_testing_suppliers()
    add_testing_categories()
    add_testing_goods()

    expense_data = add_testing_expenses()
    expense_data['elements'] = add_testing_expenses_elements(return_raw=True)
    expense = Expenses.query.filter_by(id=1).first()

    assert expense.generate_dict() == expense_data


def test_util_create_expense(app_client):
    """
    GIVEN create category & supplier utils
    WHEN calling util_create_expense()
    THEN expense is created;
         proper data is returned.
    """
    clear_db()
    util_create_expense("2023-11-01", 1, "Test supplier", "Test category", "Test units")['expense']
    queried_expense = Expenses.query.filter_by(date=datetime.datetime.strptime("2023-11-01", '%Y-%m-%d').date(),
                                             total=1, supplier=Suppliers.query.filter_by(name="Test supplier").all()[0],
                                             category=Categories.query.filter_by(name="Test category").all()[0]
                                             ).all()

    assert len(queried_expense) == 1
