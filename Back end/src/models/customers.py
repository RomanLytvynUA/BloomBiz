from src import db

class Customers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    contactInfo = db.Column(db.String(100))
    additional = db.Column(db.String(100))

    ordered_orders = db.relationship('Orders', backref='ordering_customer', lazy=True, foreign_keys='Orders.customer_id')
    received_orders = db.relationship('Orders', backref='receiving_customer', lazy=True, foreign_keys='Orders.receiver_id')

    def generate_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'contactInfo': self.contactInfo,
            'addresses': self.get_addresses(),
            'additional': self.additional,
        }
    
    def get_addresses(self):
        return list({order.customer_address for order in self.received_orders if order.customer_address})