import pytest
from src import app, db
from src.models.goods import *
from src.models.suppliers import *
from src.models.expenses import *
from src.utils.settings import util_reset_settings


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
def urls():
    domain = "http://127.0.0.1:5000"
    return {
        "get_goods": domain + "/goods/get",
        "create_product": domain + "/goods/create_product",
        "edit_product": domain + "/goods/edit_product",
        "del_product": domain + "/goods/delete_product",
        "create_category": domain + "/goods/create_category",
        "edit_category": domain + "/goods/edit_category",
        "del_category": domain + "/goods/delete_category",
        "edit_goods_price": domain + "/goods/edit_price",
        "create_decommission": domain + "/goods/create_decommission",
        "del_decommission": domain + "/goods/delete_decommission/",
        "get_decommissions": domain + "/goods/get_decommissions",
        "get_suppliers": domain + "/suppliers/get",
        "create_supplier": domain + "/suppliers/create",
        "edit_supplier": domain + "/suppliers/edit",
        "del_supplier": domain + "/suppliers/delete/",
        "get_expenses": domain + "/expenses/get",
        "create_expense": domain + "/expenses/create",
        "edit_expense": domain + "/expenses/edit",
        "del_expense": domain + "/expenses/delete/",
        "get_orders": domain + "/orders/get",
        "create_order": domain + "/orders/create",
        "edit_order": domain + "/orders/edit",
        "del_order": domain + "/orders/delete/",
    }
