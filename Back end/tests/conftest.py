import pytest
from src import app, db
from src.models.goods import *
from src.models.suppliers import *
from src.models.expenses import *
from src.models.auth import User
from src.utils.settings import util_reset_settings
from flask_jwt_extended import create_access_token
from testing_data import clear_db


@pytest.fixture
def app_client():
    client = app.test_client()

    with app.app_context():
        db.drop_all()
        db.create_all()
        util_reset_settings()

        yield client

        db.session.remove()
        db.create_all()
        util_reset_settings()


@pytest.fixture
def jwt():
    clear_db()
    with app.app_context():
        test_user = User(username="username", password="password")
        db.session.add(test_user)
        db.session.commit()
        token = create_access_token(identity=test_user.username)

    yield token


@pytest.fixture
def urls():
    domain = "http://127.0.0.1:5000"
    return {
        "get_goods": {"route": domain + "/goods/get", "method": "GET"},
        "create_product": {"route": domain + "/goods/create_product", "method": "POST"},
        "edit_product": {"route": domain + "/goods/edit_product", "method": "PUT"},
        "del_product": {"route": domain + "/goods/delete_product", "method": "DELETE"},
        "get_settings": {"route": domain + "/settings/get", "method": "GET"},
        "edit_settings": {"route": domain + "/settings/edit", "method": "PUT"},
        "reset_settings": {"route": domain + "/settings/reset", "method": "POST"},
        "create_category": {
            "route": domain + "/goods/create_category",
            "method": "POST",
        },
        "edit_category": {"route": domain + "/goods/edit_category", "method": "PUT"},
        "del_category": {
            "route": domain + "/goods/delete_category",
            "method": "DELETE",
        },
        "edit_goods_price": {"route": domain + "/goods/edit_price", "method": "POST"},
        "create_decommission": {
            "route": domain + "/goods/create_decommission",
            "method": "POST",
        },
        "del_decommission": {
            "route": domain + "/goods/delete_decommission/",
            "method": "DELETE",
        },
        "get_decommissions": {
            "route": domain + "/goods/get_decommissions",
            "method": "GET",
        },
        "get_suppliers": {"route": domain + "/suppliers/get", "method": "GET"},
        "create_supplier": {"route": domain + "/suppliers/create", "method": "POST"},
        "edit_supplier": {"route": domain + "/suppliers/edit", "method": "PUT"},
        "del_supplier": {"route": domain + "/suppliers/delete/", "method": "DELETE"},
        "get_customers": {"route": domain + "/customers/get", "method": "GET"},
        "create_customer": {"route": domain + "/customers/create", "method": "POST"},
        "edit_customer": {"route": domain + "/customers/edit", "method": "PUT"},
        "del_customer": {"route": domain + "/customers/delete/", "method": "DELETE"},
        "get_expenses": {"route": domain + "/expenses/get", "method": "GET"},
        "create_expense": {"route": domain + "/expenses/create", "method": "POST"},
        "edit_expense": {"route": domain + "/expenses/edit", "method": "PUT"},
        "del_expense": {"route": domain + "/expenses/delete/", "method": "DELETE"},
        "get_orders": {"route": domain + "/orders/get", "method": "GET"},
        "create_order": {"route": domain + "/orders/create", "method": "POST"},
        "edit_order": {"route": domain + "/orders/edit", "method": "PUT"},
        "del_order": {"route": domain + "/orders/delete/", "method": "DELETE"},
        "login": {"route": domain + "/auth/login", "method": "POST"},
        "register": {"route": domain + "/auth/register", "method": "POST"},
    }
