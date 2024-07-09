from .. import db
from flask import jsonify, request, Blueprint
from src.models.expenses import Expenses, ExpensesElements
from src.models.goods import Goods
from ..utils.suppliers import util_create_supplier
from ..utils.goods import util_create_product
from ..utils.expenses import util_create_expense
from flask_jwt_extended import verify_jwt_in_request


expenses = Blueprint("expenses", __name__)


@expenses.before_request
def before_request_func():
    verify_jwt_in_request()


@expenses.route("/get", methods=["GET"])
def get_expenses():
    data = [
        expense.generate_dict()
        for expense in Expenses.query.order_by(Expenses.id.desc()).all()
    ]
    return jsonify(data)


@expenses.route("/create", methods=["POST"])
def create_expense():
    expense_data = request.get_json()

    required_data = {"date", "total", "supplier", "category", "elements"}
    if not len(required_data - set(expense_data.keys())):
        new_expense_data = util_create_expense(
            date=expense_data["date"],
            total=expense_data["total"],
            supplier=expense_data["supplier"],
            category=expense_data["category"],
            units=expense_data.get("categoryUnits", ""),
        )
        new_expense_obj = new_expense_data["expense"]
        for element in expense_data["elements"]:
            new_element = ExpensesElements(
                quantity=element["quantity"],
                price=element["price"],
                product=util_create_product(
                    element.get("product"), new_expense_obj.category
                )["product"],
                expense=new_expense_obj,
            )
            db.session.add(new_element)
        db.session.commit()

        changes = {
            "expenses": [new_expense_obj.generate_dict()],
            "suppliers": (
                [new_expense_obj.supplier.generate_dict()]
                if new_expense_data["supplier_changes_applied"]
                else []
            ),
            "categories": (
                [new_expense_obj.category.generate_dict()]
                if new_expense_data["category_changes_applied"]
                else []
            ),
            # add all products from expense elements to changes since new products might have been added and price needs to be recalculated
            "goods": [
                element.product.generate_dict() for element in new_expense_obj.elements
            ],
        }

        return jsonify(changes), 200
    return "Missing required data.", 406


@expenses.route("/edit", methods=["PUT"])
def edit_expense():
    expense_data = request.get_json()

    required_data = {"expense_id", "date", "total", "supplier", "elements"}
    if not len(required_data - set(expense_data.keys())):
        changes = {}

        # change expense properties
        expense = Expenses.query.filter_by(id=expense_data["expense_id"]).all()[0]
        expense.date = expense_data["date"]
        expense.total = expense_data["total"]
        supplier_data = util_create_supplier(expense_data["supplier"])
        expense.supplier = supplier_data["supplier"]
        changes["suppliers"] = (
            [expense.supplier.generate_dict()]
            if supplier_data["changes_applied"]
            else []
        )
        db.session.add(expense)
        db.session.commit()

        # delete old elements
        deleted_products_id = []
        for element in ExpensesElements.query.filter_by(expense=expense).all():
            deleted_products_id.append(element.product.id)
            db.session.delete(element)
        db.session.commit()

        # add deleted elements to changes so that the prices are recalculated
        deleted_goods = Goods.query.filter(Goods.id.in_(deleted_products_id)).all()
        changes["goods"] = [product.generate_dict() for product in deleted_goods]

        # add new elements
        for element in expense_data["elements"]:
            new_element = ExpensesElements(
                quantity=element["quantity"],
                price=element["price"],
                product=util_create_product(element.get("product"), expense.category)[
                    "product"
                ],
                expense=expense,
            )
            db.session.add(new_element)
        db.session.commit()

        # must add expense to changes only after adding expense elements
        changes["expenses"] = [expense.generate_dict()]

        # add all products from expense elements to changes since new products might have been added, prices needs to be recalculated
        for element in expense.elements:
            # remove old product from changes if it is there
            for product_changed in changes["goods"]:
                if product_changed["id"] == element.product.id:
                    changes["goods"].remove(product_changed)
                    break
            changes["goods"].append(element.product.generate_dict())

        return jsonify(changes), 200
    return "Missing required data.", 406


@expenses.route("/delete/<expense_id>", methods=["DELETE"])
def delete_expense(expense_id):
    expense = Expenses.query.filter_by(id=expense_id).all()

    if len(expense):
        db.session.delete(expense[0])
        db.session.commit()

        return "Expense deleted successfully.", 200
    return "Failed to fetch the expense with given id.", 406
