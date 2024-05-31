from .. import db
from ..models.customers import Customers


def util_create_customer(name, contact_info, address='', additional=''):
    customer = Customers.query.filter_by(contactInfo=contact_info).all()
    if not len(customer):
        new_customer = Customers(name=name, contactInfo=contact_info, address=address, additional=additional)
        db.session.add(new_customer)
        db.session.commit()

        return {'customer': new_customer,
                'message': 'Created new customer successfully.'}
    else:
        return {'customer': customer,
                'message': 'Customer with contacts already exists.'}

