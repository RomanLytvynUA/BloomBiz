from src import db
from .expenses import Expenses


class Suppliers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    contactInfo = db.Column(db.String(100))
    additional = db.Column(db.String(100))

    expenses = db.relationship('Expenses', cascade="all,delete", backref='supplier', lazy=True)

    def generate_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'contactInfo': self.contactInfo,
            'additional': self.additional,
        }
