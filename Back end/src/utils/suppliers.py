from .. import db
from ..models.suppliers import Suppliers


def util_create_supplier(name, contact_info='-', additional='-'):
    supplier = Suppliers.query.filter_by(name=name).all()
    if not len(supplier):
        new_supplier = Suppliers(name=name, contactInfo=contact_info, additional=additional)
        db.session.add(new_supplier)
        db.session.commit()

        return {'supplier': new_supplier,
                'changes_applied': True,
                'message': 'Created new supplier successfully.'}
    else:
        return {'supplier': supplier[0],
                'changes_applied': False,
                'message': 'Supplier with this name already exists.'}


def util_edit_supplier(supplier_id, name, contact_info, additional):
    supplier = Suppliers.query.filter_by(id=supplier_id).all()
    if len(supplier):
        supplier[0].name = name
        supplier[0].contactInfo = contact_info
        supplier[0].additional = additional

        db.session.add(supplier[0])
        db.session.commit()
        return {'supplier': supplier[0],
                'changes_applied': True,
                'message': "Edited supplier successfully."}
    else:
        return {'supplier': None,
                'changes_applied': False,
                'message': "Failed to fetch supplier."}
