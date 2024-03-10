from .. import db
from ..models.suppliers import Suppliers


def util_create_supplier(name, contact_info='-', additional='-'):
    supplier_names = [name for name, in Suppliers.query.with_entities(Suppliers.name).all()]
    if name not in supplier_names:
        new_supplier = Suppliers(name=name, contactInfo=contact_info, additional=additional)
        db.session.add(new_supplier)
        db.session.commit()

        return {'supplier': new_supplier,
                'message': 'Created new supplier successfully.'}
    else:
        return {'supplier': Suppliers.query.filter_by(name=name).all()[0],
                'message': 'Supplier with this name already exists.'}


def util_edit_supplier(supplier_id, name, contact_info, additional):
    supplier = Suppliers.query.filter_by(id=supplier_id).all()
    if len(supplier):
        supplier[0].name = name
        supplier[0].contactInfo = contact_info
        supplier[0].additional = additional

        db.session.add(supplier[0])
        db.session.commit()
        return {'supplier': supplier[0], 'message': "Edited supplier successfully."}
    else:
        return {'supplier': None, 'message': "Failed to fetch supplier."}
