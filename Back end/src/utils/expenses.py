from .. import db
from ..models.goods import Expenses
from .suppliers import util_create_supplier
from .goods import util_create_category, util_create_product


def util_create_expense(date, total, supplier, category, units):
    expense = Expenses(date=date, total=total, supplier=util_create_supplier(supplier)['supplier'],
                       category=util_create_category(category, units)['category'])
    db.session.add(expense)
    return {'expense': expense,
            'message': 'Created new expense successfully.'}


# def util_create_product(name, category):
#     product = Goods.query.filter_by(name=name, category=category).all()
#     if not len(product):
#         new_product = Goods(name=name, category=category)
#         db.session.add(new_product)
#         db.session.commit()
#
#         return {'product': new_product,
#                 'message': 'Created new product successfully.'}
#     else:
#         return {'product': product[0],
#                 'message': 'Product with this name already exists.'}
