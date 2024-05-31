from src import db
from .customers import Customers


class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    status = db.Column(db.String(100))
    discount = db.Column(db.Float)
    price = db.Column(db.Float)
    
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id', ondelete='CASCADE'), nullable=True)
    receiver_id = db.Column(db.Integer, db.ForeignKey('customers.id', ondelete='CASCADE'), nullable=True)

    elements = db.relationship('OrdersElements', backref='order', passive_deletes=True, lazy=True)


    def generate_dict(self):
        return {
            'id': self.id,
            'date': self.date.strftime('%a, %d %b %Y %H:%M:%S GMT'),
            'status': self.status,
            'discount': self.discount,
            'price': self.price,
            'customer': self.ordering_customer.generate_dict(),
            'receiver': self.receiving_customer.generate_dict(),
            'elements': self.generate_elements_dict(),
        }

    def generate_elements_dict(self):
        elements_dict = {}
        for element in self.elements:
            category = element.product.category.name
            if category in elements_dict.keys():
                elements_dict[category].append(element.generate_dict())
            else:
                elements_dict[category] = []
                elements_dict[category].append(element.generate_dict())
        return elements_dict


class OrdersElements(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Float)
    price = db.Column(db.Float)

    order_id = db.Column(db.Integer, db.ForeignKey('orders.id', ondelete='CASCADE'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('goods.id', ondelete='CASCADE'), nullable=False)

    def generate_dict(self):
        return {
            'id': self.id,
            'quantity': self.quantity,
            'price': self.price,
            'product': self.product_id,
            'order': self.order_id,
        }
