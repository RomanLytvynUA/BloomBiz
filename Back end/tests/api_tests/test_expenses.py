import json
import requests
from src.models.expenses import Expenses, ExpensesElements
from tests.testing_data import (
    clear_db,
    add_testing_expenses,
    add_testing_category,
    add_testing_goods,
    add_testing_suppliers,
    add_testing_expenses_elements,
)


def test_get_expenses(urls, app_client, jwt):
    """
    GIVEN db with supplier, categories, goods, expenses instances
    WHEN calling get expenses endpoint
    THEN proper data is returned
    """
    route = urls["get_expenses"]

    clear_db()
    add_testing_suppliers()
    add_testing_category()
    add_testing_goods()
    add_testing_expenses()
    expense = add_testing_expenses_elements()

    response = requests.request(
        url=route["route"],
        method=route["method"],
        headers={"Authorization": f"Bearer {jwt}"},
    )

    assert json.loads(response.text) == [expense]


def test_create_expense(urls, app_client, jwt):
    """
    GIVEN supplier, category, goods instances
    WHEN calling create expense endpoint
    THEN new expense is added;
         proper changes are returned.
    PROVIDED all required data is present
    """
    route = urls["create_expense"]

    clear_db()
    supplier = add_testing_suppliers()[0]["name"]
    category = add_testing_category()["name"]
    products = add_testing_goods()
    data = {
        "date": "2023/11/1",
        "total": 1,
        "supplier": supplier,
        "category": category,
        "elements": [
            {"product": products[0], "quantity": 2, "price": 3},
            {"product": products[1], "quantity": 4, "price": 5},
        ],
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

    expense = Expenses.query.filter(
        Expenses.date == data["date"],
        Expenses.total == 1,
        Expenses.supplier.has(name=supplier),
        Expenses.category.has(name=category),
    ).all()
    expenses_elements = ExpensesElements.query.filter_by(expense=expense[0]).all()

    assert not len(
        {"categories", "expenses", "suppliers", "goods"}
        - set(json.loads(positive_response.text).keys())
    )
    assert positive_response.status_code == 200
    assert negative_response.status_code == 406
    assert len(expenses_elements) == 2
    assert expenses_elements[0].generate_dict() == {
        "id": 1,
        "quantity": 2.0,
        "price": 3.0,
        "product": 1,
        "expense": expense[0].id,
    }
    assert expenses_elements[1].generate_dict() == {
        "id": 2,
        "quantity": 4.0,
        "price": 5.0,
        "product": 2,
        "expense": expense[0].id,
    }


def test_edit_expense(urls, app_client, jwt):
    """
    GIVEN db with an expense instance
    WHEN calling edit expense endpoint
    THEN expense is edited;
         proper changes are returned.
    PROVIDED all required data is present
    """
    route = urls["edit_expense"]

    clear_db()
    add_testing_suppliers()
    add_testing_category()
    add_testing_goods()
    add_testing_expenses()
    expense = add_testing_expenses_elements()
    data = {
        "expense_id": expense["id"],
        "date": "2023/11/1",
        "total": 1,
        "supplier": "Supplier2",
        "elements": [{"product": "Product3", "quantity": 2, "price": 3}],
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

    edited_expense = Expenses.query.filter(
        Expenses.id == data["expense_id"],
        Expenses.date == data["date"],
        Expenses.total == data["total"],
        Expenses.supplier.has(name=data["supplier"]),
    ).all()
    expenses_elements = ExpensesElements.query.filter_by(
        expense=edited_expense[0]
    ).all()

    assert not len(
        {"expenses", "suppliers", "goods"}
        - set(json.loads(positive_response.text).keys())
    )
    assert positive_response.status_code == 200
    assert negative_response.status_code == 406
    assert len(edited_expense)
    assert len(expenses_elements) == 1
    assert expenses_elements[0].generate_dict() == {
        "product": 3,
        "quantity": 2.0,
        "price": 3.0,
        "id": expenses_elements[0].id,
        "expense": expenses_elements[0].expense.id,
    }


def test_del_expense(urls, app_client, jwt):
    """
    GIVEN db with an expense instance
    WHEN calling delete expense endpoint
    THEN expense is deleted
    """
    route = urls["del_expense"]

    clear_db()
    add_testing_suppliers()
    add_testing_category()
    add_testing_goods()
    add_testing_expenses()
    expense_data = add_testing_expenses_elements()

    response = requests.request(
        url=route["route"] + str(expense_data["id"]),
        method=route["method"],
        headers={"Authorization": f"Bearer {jwt}"},
    )
    expense = Expenses.query.filter_by(id=expense_data["id"]).all()

    assert response.status_code == 200
    assert not len(expense)
