from .. import db
from flask import jsonify, request, Blueprint
from src.models.expenses import Expenses, ExpensesElements
from ..utils.suppliers import util_create_supplier
from ..utils.goods import util_create_category, util_create_product
from ..utils.expenses import util_create_expense

expenses = Blueprint("expenses", __name__)


@expenses.route('/get', methods=['GET'])
def get_expenses():
    data = [expense.generate_dict() for expense in Expenses.query.order_by(Expenses.id.desc()).all()]
    return jsonify(data)


@expenses.route('/create', methods=['POST'])
def create_expense():
    expense_data = request.get_json()

    required_data = {'date', 'total', 'supplier', 'category', "elements"}
    if not len(required_data - set(expense_data.keys())):
        date = expense_data['date']
        total = expense_data['total']
        supplier = expense_data['supplier']
        category = expense_data['category']
        expense_elements = expense_data['elements']
        units = ''
        if expense_data.get('categoryUnits') is not None: units = expense_data['categoryUnits']

        expense = util_create_expense(date=date, total=total, supplier=supplier,
                                      category=category, units=units)['expense']

        # Looping through each element of a copy of expense elements list where product string is either
        # replaced with an existing object of goods or fresh created one.
        for element in [dict(element, product=util_create_product(element.get('product'), expense.category)['product'])
                        for element in expense_elements]:
            new_element = ExpensesElements(quantity=element['quantity'], price=element['price'],
                                           product=element['product'], expense=expense)
            db.session.add(new_element)
        db.session.commit()

        return "Created new expense successfully.", 200
    return "Missing required data.", 406


@expenses.route('/edit', methods=['PUT'])
def edit_expense():
    expense_data = request.get_json()

    required_data = {'expense_id', 'date', 'total', 'supplier', "elements"}
    if not len(required_data - set(expense_data.keys())):
        expense_id = expense_data['expense_id']
        date = expense_data['date']
        total = expense_data['total']
        supplier = expense_data['supplier']
        expense_elements = expense_data['elements']

        expense = Expenses.query.filter_by(id=expense_id).all()[0]
        expense.date = date
        expense.total = total
        expense.supplier = util_create_supplier(supplier)['supplier']
        db.session.add(expense)

        for element in ExpensesElements.query.filter_by(expense=expense).all():
            db.session.delete(element)

        # Looping through each element of a copy of expense elements list where product string is either
        # replaced with an existing object of goods or fresh created one.
        for element in [dict(element, product=util_create_product(element.get('product'), expense.category)['product'])
                        for element in expense_elements]:
            new_element = ExpensesElements(quantity=element['quantity'], price=element['price'],
                                           product=element['product'], expense=expense)
            db.session.add(new_element)
        db.session.commit()

        return "Edited expense successfully.", 200
    return "Missing required data.", 406


@expenses.route('/delete/<expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    expense = Expenses.query.filter_by(id=expense_id).all()

    if len(expense):
        db.session.delete(expense[0])
        db.session.commit()

        return "Expense deleted successfully.", 200
    return "Failed to fetch the expense with given id.", 406
