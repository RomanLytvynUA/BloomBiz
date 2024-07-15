import datetime
from src import db, app
from sqlalchemy import text
from src.models.goods import *
from src.models.suppliers import *
from src.models.expenses import *
from src.models.orders import *
from src.models.customers import *
from src.models.auth import *


def clear_db():
    with app.app_context():
        db.session.query(Categories).delete()
        db.session.query(Suppliers).delete()
        db.session.query(Expenses).delete()
        db.session.query(Orders).delete()
        db.session.query(User).delete()
        db.session.query(RegistrationCode).delete()
        db.session.commit()


def add_testing_category():
    with app.app_context():
        categories_data = [
            {"name": "Category", "units": "units"},
        ]

        db.session.query(Categories).delete()
        db.session.execute(text(f"ALTER SEQUENCE categories_id_seq RESTART WITH 1"))
        db.session.commit()

        for data in categories_data:
            category = Categories(**data)
            db.session.add(category)
            db.session.commit()
            data["id"] = category.id

        return {
            "name": categories_data[0]["name"],
            "id": categories_data[0]["id"],
            "units": categories_data[0]["units"],
        }


def add_testing_goods(return_obj_dict=False):
    with app.app_context():
        category = Categories.query.filter_by(id=1).first()

        goods_data = [
            {"category": category, "name": "Product1"},
            {"category": category, "name": "Product2"},
        ]

        goods_dict = []

        db.session.query(Goods).delete()
        db.session.execute(text(f"ALTER SEQUENCE goods_id_seq RESTART WITH 1"))
        db.session.commit()

        for data in goods_data:
            product = Goods(**data)
            db.session.add(product)
            db.session.commit()
            goods_dict.append(product.generate_dict())

        if return_obj_dict:
            return goods_dict
        return [product["name"] for product in goods_data]


def add_testing_suppliers():
    with app.app_context():
        suppliers_data = [
            {"name": "Supplier", "contactInfo": "phone", "additional": "comment"},
        ]

        db.session.query(Suppliers).delete()
        db.session.execute(text("ALTER SEQUENCE suppliers_id_seq RESTART WITH 1"))
        db.session.commit()

        for data in suppliers_data:
            supplier = Suppliers(**data)
            db.session.add(supplier)
            db.session.commit()
            data["id"] = supplier.id

        return [supplier for supplier in suppliers_data]


def add_testing_expenses():
    with app.app_context():
        supplier = Suppliers.query.filter_by(id=1).first()
        category = Categories.query.filter_by(id=1).first()

        expenses_data = [
            {
                "date": "2023-11-01",
                "supplier": supplier,
                "category": category,
                "total": 0.0,
            },
        ]

        db.session.query(Expenses).delete()
        db.session.execute(text("ALTER SEQUENCE expenses_id_seq RESTART WITH 1"))
        db.session.commit()

        for data in expenses_data:
            expense = Expenses(**data)
            db.session.add(expense)
        db.session.commit()

        return {
            "id": 1,
            "date": datetime.datetime.strptime(expenses_data[0]["date"], "%Y-%m-%d")
            .date()
            .strftime("%a, %d %b %Y %H:%M:%S GMT"),
            "total": expenses_data[0]["total"],
            "supplier": expenses_data[0]["supplier"].id,
            "category": expenses_data[0]["category"].id,
        }


def add_testing_expenses_elements(return_raw=False):
    with app.app_context():
        expense = Expenses.query.filter_by(id=1).first()
        product1 = Goods.query.filter_by(id=1).first()
        product2 = Goods.query.filter_by(id=2).first()

        expense_elements = [
            {"expense": expense, "product": product1, "quantity": 2.0, "price": 2.0},
            {"expense": expense, "product": product2, "quantity": 1.0, "price": 2.0},
        ]

        db.session.query(ExpensesElements).delete()
        db.session.execute(
            text("ALTER SEQUENCE expenses_elements_id_seq RESTART WITH 1")
        )
        db.session.commit()

        for data in expense_elements:
            element = ExpensesElements(**data)
            db.session.add(element)
            db.session.commit()
            data["id"] = element.id

        if return_raw:
            for element in expense_elements:
                element["expense"] = expense.id
                element["product"] = element["product"].id
            return expense_elements
        return expense.generate_dict()


def add_testing_customers():
    with app.app_context():
        customers_data = [
            {"name": "Name", "contactInfo": "+380000000000", "additional": "text"},
        ]

        db.session.query(Customers).delete()
        db.session.execute(text("ALTER SEQUENCE customers_id_seq RESTART WITH 1"))
        db.session.commit()

        for data in customers_data:
            customer = Customers(**data)
            db.session.add(customer)
            db.session.commit()
            data["id"] = customer.id

        return customers_data


def add_testing_orders(customer_id):
    with app.app_context():
        orders_data = [
            {
                "date": "2023-11-01",
                "status": "Status",
                "price": 1.0,
                "discount": 2.0,
                "additional": "",
                "customer_address": "Address",
                "customer_id": customer_id,
                "receiver_id": customer_id,
            },
        ]

        db.session.query(Orders).delete()
        db.session.execute(text("ALTER SEQUENCE orders_id_seq RESTART WITH 1"))
        db.session.commit()

        for data in orders_data:
            order = Orders(**data)
            db.session.add(order)
            db.session.commit()
            data["id"] = order.id
        orders_data[0]["date"] = (
            datetime.datetime.strptime(orders_data[0]["date"], "%Y-%m-%d")
            .date()
            .strftime("%a, %d %b %Y %H:%M:%S GMT")
        )
        return orders_data


def add_testing_orders_elements(return_raw=False):
    with app.app_context():
        order = Orders.query.filter_by(id=1).first()
        product1 = Goods.query.filter_by(id=1).first()
        product2 = Goods.query.filter_by(id=2).first()

        orders_elements = [
            {"order": order, "product": product1, "quantity": 0.0, "price": 2.0},
            {"order": order, "product": product2, "quantity": 1.0, "price": 2.0},
        ]

        db.session.query(OrdersElements).delete()
        db.session.execute(text("ALTER SEQUENCE orders_elements_id_seq RESTART WITH 1"))
        db.session.commit()

        for data in orders_elements:
            element = OrdersElements(**data)
            db.session.add(element)
            db.session.commit()
            data["id"] = element.id

        if return_raw:
            for element in orders_elements:
                element["product"] = element["product"].id
                element["order"] = element["order"].id
            elements_dict = {product1.category.name: orders_elements}
            return elements_dict
        return order.generate_dict()


def add_testing_decommissions():
    with app.app_context():
        product1 = Goods.query.filter_by(id=1).first()

        decommissions_elements = [
            {"date": "2023-11-01", "product": product1, "quantity": 1.0},
        ]

        db.session.query(Decommissions).delete()
        db.session.execute(text("ALTER SEQUENCE decommissions_id_seq RESTART WITH 1"))
        db.session.commit()

        for data in decommissions_elements:
            element = Decommissions(**data)
            db.session.add(element)
            db.session.commit()
            data["id"] = element.id
            data["product"] = product1.name
            data["date"] = datetime.date(2023, 11, 1).strftime(
                "%a, %d %b %Y %H:%M:%S GMT"
            )

        return decommissions_elements
