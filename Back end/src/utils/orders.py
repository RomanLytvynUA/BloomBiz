from .. import db
from ..models.orders import Orders
from .goods import util_create_category, util_create_product


def util_create_order(date, discount, price, status):
    order = Orders(date=date, discount=discount, price=price, status=status)
    db.session.add(order)
    return {'order': order,
            'message': 'Created new order successfully.'}


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
