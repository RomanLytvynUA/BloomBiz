from src import db


class Expenses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    total = db.Column(db.Float)

    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id', ondelete='CASCADE'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete='CASCADE'), nullable=False)

    elements = db.relationship('ExpensesElements', backref='expense', passive_deletes=True, lazy=True)

    def generate_dict(self):
        return {
            'id': self.id,
            'date': self.date.strftime('%a, %d %b %Y %H:%M:%S GMT'),
            'total': self.total,
            'supplier': self.supplier_id,
            'category': self.category_id,
            'elements': [element.generate_dict() for element in self.elements],
        }


class ExpensesElements(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Float)
    price = db.Column(db.Float)

    expense_id = db.Column(db.Integer, db.ForeignKey('expenses.id', ondelete='CASCADE'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('goods.id', ondelete='CASCADE'), nullable=False)

    def generate_dict(self):
        return {
            'id': self.id,
            'quantity': self.quantity,
            'price': self.price,
            'product': self.product_id,
            'expense': self.expense_id,
        }
