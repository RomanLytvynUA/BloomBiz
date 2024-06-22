from .. import db
from ..models.customers import Customers


def util_create_customer(name, contact_info, additional=''):
    customer = Customers.query.filter_by(contactInfo=str(contact_info)).all()
    if not len(customer):
        new_customer = Customers(name=str(name), contactInfo=str(contact_info), additional=str(additional))
        db.session.add(new_customer)
        db.session.commit()

        return {'customer': new_customer,
                'message': 'Created new customer successfully.'}
    else:
        return {'customer': customer[0],
                'message': 'Customer with contacts already exists.'}


def util_edit_customer(id, name, contact_info, additional=''):
    customer = Customers.query.filter_by(id=id).all()
    if len(customer):
        customer[0].name = name
        customer[0].contactInfo = contact_info
        customer[0].additional = additional
        db.session.add(customer[0])
        db.session.commit()

        return {'customer': customer[0],
                'message': 'Edited customer successfully.'}
    else:
        return {'customer': customer[0],
                'message': 'Failed to fetch a customer with given id.'}

