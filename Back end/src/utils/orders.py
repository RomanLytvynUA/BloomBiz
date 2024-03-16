from .. import db
from ..models.orders import Orders


def util_create_order(date, discount, price, status):
    order = Orders(date=date, discount=discount, price=price, status=status)
    db.session.add(order)
    return {'order': order,
            'message': 'Created new order successfully.'}
