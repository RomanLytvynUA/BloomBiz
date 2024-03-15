from .. import db
from ..models.goods import Expenses
from .suppliers import util_create_supplier
from .goods import util_create_category


def util_create_expense(date, total, supplier, category, units):
    expense = Expenses(date=date, total=total, supplier=util_create_supplier(supplier)['supplier'],
                       category=util_create_category(category, units)['category'])
    db.session.add(expense)
    return {'expense': expense,
            'message': 'Created new expense successfully.'}
