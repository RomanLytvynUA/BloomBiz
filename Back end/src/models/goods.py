from src import db
from .expenses import Expenses, ExpensesElements
from .orders import OrdersElements


class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    units = db.Column(db.String(100))

    goods = db.relationship('Goods', backref='category', passive_deletes=True, lazy=True)
    expenses = db.relationship('Expenses', backref='category', passive_deletes=True, lazy=True)

    def generate_dict(self):
        sorted_goods = sorted(self.goods, key=lambda product: product.id)
        return {
            'id': self.id,
            'name': self.name,
            'units': self.units,
            'goods': [product.generate_dict() for product in sorted_goods],
        }


class Goods(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Float, nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete='CASCADE'), nullable=False)

    expenses_elements = db.relationship('ExpensesElements', backref='product', passive_deletes=True, lazy=True)
    decommissions_elements = db.relationship('Decommissions', backref='product', passive_deletes=True, lazy=True)
    orders_elements = db.relationship('OrdersElements', backref='product', passive_deletes=True, lazy=True)

    def generate_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category_id,
        }


class Decommissions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    product_id = db.Column(db.Integer, db.ForeignKey('goods.id', ondelete='CASCADE'), nullable=False)
    quantity = db.Column(db.Float)

    def generate_dict(self):
        return {
            'id': self.id,
            'date': self.date.strftime('%a, %d %b %Y %H:%M:%S GMT'),
            'product': Goods.query.filter_by(id=self.product_id).first().name,
            'quantity': self.quantity,
        }
