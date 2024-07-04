from .. import db
from ..models.goods import Expenses
from .suppliers import util_create_supplier
from .goods import util_create_category


def util_create_expense(date, total, supplier, category, units):
    supplierObj = util_create_supplier(supplier)
    categoryObj = util_create_category(category, units)
    expense = Expenses(date=date, total=total, supplier=supplierObj['supplier'],
                       category=categoryObj['category'])
    db.session.add(expense)
    return {'expense': expense,
            'supplier_changes_applied': True if supplierObj['changes_applied'] else False,
            'category_changes_applied': True if categoryObj['changes_applied'] else False,
            'message': 'Created new expense successfully.'}
