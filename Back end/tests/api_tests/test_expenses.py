import json
import requests
from src.models.expenses import Expenses, ExpensesElements
from tests.testing_data import clear_db, add_testing_expenses, \
    add_testing_categories, add_testing_goods, add_testing_suppliers, \
    add_testing_expenses_elements


def test_get_expenses(urls):
    """
    GIVEN db with supplier, categories, goods, expenses instances
    WHEN calling get expenses endpoint
    THEN proper data is returned
    """
    url = urls["get_expenses"]

    clear_db()
    add_testing_suppliers()
    add_testing_categories()
    add_testing_goods()
    add_testing_expenses()
    expense = add_testing_expenses_elements()

    response = requests.get(url=url)

    assert json.loads(response.text) == [expense]


def test_create_expense(urls, app_client):
    """
    GIVEN supplier, category, goods instances
    WHEN calling create expense endpoint
    THEN new expense is added
    PROVIDED all required data is present
    """
    url = urls["create_expense"]

    clear_db()
    supplier = add_testing_suppliers()[0]['name']
    category = add_testing_categories()['name']
    products = add_testing_goods()
    data = {'date': "2023/11/1", 'total': 1, 'supplier': supplier, 'category': category, "elements": [
        {'product': products[0], 'quantity': 2, 'price': 3},
        {'product': products[1], 'quantity': 3, 'price': 4},
    ]}

    positive_response = requests.post(url=url, json=data, headers={"Content-Type": "application/json"})
    negative_response = requests.post(url=url, json={}, headers={"Content-Type": "application/json"})

    expense = Expenses.query.filter(Expenses.date == data['date'], Expenses.total == 1,
                                    Expenses.supplier.has(name=supplier), Expenses.category.has(name=category)).all()
    expenses_elements = ExpensesElements.query.filter_by(expense=expense[0]).all()

    assert positive_response.status_code == 200
    assert negative_response.status_code == 406
    assert len(supplier)
    assert len(expenses_elements) == 2
    assert expenses_elements[0].generate_dict() == {'id': 1,
                                                    'quantity': 2.0,
                                                    'price': 3.0,
                                                    'product': 1,
                                                    'expense': expense[0].id,
                                                    }


def test_edit_expense(urls, app_client):
    """
    GIVEN db with an expense instance
    WHEN calling edit expense endpoint
    THEN expense is edited
    PROVIDED all required data is present
    """
    url = urls["edit_expense"]

    clear_db()
    add_testing_suppliers()
    add_testing_categories()
    add_testing_goods()
    add_testing_expenses()
    expense = add_testing_expenses_elements()
    data = {'expense_id': expense['id'], 'date': "2023/11/1", 'total': 1, 'supplier': "Supplier2",
            "elements": [{'product': "Product3", 'quantity': 2, 'price': 3}]}

    positive_response = requests.put(url=url, json=data, headers={"Content-Type": "application/json"})
    negative_response = requests.put(url=url, json={}, headers={"Content-Type": "application/json"})

    edited_expense = Expenses.query.filter_by(id=expense['id']).all()
    expenses_elements = ExpensesElements.query.filter_by(expense=edited_expense[0]).all()

    assert positive_response.status_code == 200
    assert negative_response.status_code == 406
    assert len(edited_expense)
    assert len(expenses_elements) == 1


def test_del_expense(urls, app_client):
    """
    GIVEN db with an expense instance
    WHEN calling delete expense endpoint
    THEN expense is deleted
    """
    url = urls["del_expense"]

    clear_db()
    add_testing_suppliers()
    add_testing_categories()
    add_testing_goods()
    add_testing_expenses()
    expense_data = add_testing_expenses_elements()

    response = requests.delete(url=url+str(expense_data['id']))
    expense = Expenses.query.filter_by(id=expense_data['id']).all()

    assert response.status_code == 200
    assert not len(expense)
