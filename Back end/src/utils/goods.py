from .. import db
from ..models.goods import Goods, Categories, Decommissions
from ..models.orders import OrdersElements
from ..models.expenses import ExpensesElements
from ..models.settings import Settings


def util_create_category(name, units):
    category = Categories.query.filter_by(name=name).all()
    if not len(category):
        new_category = Categories(name=name, units=units)
        db.session.add(new_category)
        db.session.commit()

        return {'category': new_category,
                'message': 'Created new category successfully.'}
    else:
        return {'category': category[0],
                'message': 'Category with this name already exists.'}


def util_create_product(name, category):
    product = Goods.query.filter_by(name=name, category=category).all()
    if not len(product):
        new_product = Goods(name=name, category=category)
        db.session.add(new_product)
        db.session.commit()
        
        return {'product': new_product,
                'message': 'Created new product successfully.'}
    else:
        return {'product': product[0],
                'message': 'Product with this name already exists.'}


def util_create_decommission(product, date, quantity, category):
    category = Categories.query.filter_by(name=category).all()
    if len(category):
        new_decommission = Decommissions(product=util_create_product(product, category[0])['product'],
                                         quantity=quantity, date=date)
        db.session.add(new_decommission)
        db.session.commit()

        return {'decommission': new_decommission,
                'message': 'Created new decommission successfully.'}
    else:
        return {'message': 'Failed to fetch provided category.'}


def util_set_product_price(product_id, price):
    product = Goods.query.filter_by(id=product_id).all()
    if len(product):
        if price == "RESET":
            product[0].price = None
            db.session.add(product[0])
            db.session.commit()
            return {'message': 'Set price successfully.'}

        product[0].price = price
        db.session.add(product[0])
        db.session.commit()
        return {'message': 'Set price successfully.'}
    else:
        return {'message': 'Failed to fetch product with provided id.'}


def util_calc_instock():
    in_stock_goods = []
    margin = int(Settings.query.filter_by(name='defaultMargin').first().value)
    all_goods = Goods.query.order_by(Goods.id).all()

    for product in all_goods:
        quantity = 0
        price = 0

        bought_goods = ExpensesElements.query.filter_by(product=product).order_by(ExpensesElements.id).all()
        for bought_product in bought_goods:
            quantity += bought_product.quantity
            price = round(bought_product.price*(margin+100)/100)

        decommissioned_goods = Decommissions.query.filter_by(product=product).all()
        for decommissioned_product in decommissioned_goods:
            quantity -= decommissioned_product.quantity

        order_goods = OrdersElements.query.filter_by(product=product).all()
        for order_product in order_goods:
            quantity -= order_product.quantity

        # Convert quantity to int if it's no float part
        if quantity - int(quantity) == 0: quantity = int(quantity)
        # Set price to custom if it's specified in the db
        if product.price is not None: price = product.price

        in_stock_goods.append({'category': product.category.name, 'category_id': product.category.id,
                               'product': product.name, 'quantity': quantity, 'id': product.id,
                               'units': product.category.units, 'price': price})
    return sorted(in_stock_goods, key=lambda obj: obj['category_id'])
