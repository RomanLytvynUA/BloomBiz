from .. import db
from ..models.orders import Orders


def util_create_order(date, discount, price, status, address='', customer=None, receiver=None):
    order = Orders(date=date, discount=discount, price=price, status=status, customer_address=address)
    if customer is not None:
        order.customer_id = customer.id
        if receiver is not None and receiver is not None:
            order.customer_id = customer.id
            order.receiver_id = receiver.id
    
    db.session.add(order)
    return {'order': order,
            'message': 'Created new order successfully.'}
