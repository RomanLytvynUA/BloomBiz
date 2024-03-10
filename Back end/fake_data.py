import random
from src import db, app
from sqlalchemy import text
from src.models.goods import *
from src.models.suppliers import *
from src.models.expenses import *
from src.models.orders import *


def add_categories():
    categories_data = [
        {'name': 'Квіти', 'units': 'шт.'},
        {'name': 'Упаковка', 'units': 'м.'},
        {'name': 'Іграшки', 'units': 'шт.'},
    ]

    db.session.query(Categories).delete()
    db.session.execute(text(f"ALTER SEQUENCE categories_id_seq RESTART WITH 1"))

    for data in categories_data:
        category = Categories(**data)
        db.session.add(category)

    db.session.commit()


def add_goods():
    flowers = Categories.query.filter_by(id=1).first()
    packing = Categories.query.filter_by(id=2).first()
    toys = Categories.query.filter_by(id=3).first()

    goods_data = [
        # Id 1 - 50
        {'category': flowers, 'name': 'Білі троянди'},
        {'category': flowers, 'name': 'Червоні троянди'},
        {'category': flowers, 'name': 'Рожеві троянди'},
        {'category': flowers, 'name': 'Фіолетові троянди'},
        {'category': flowers, 'name': 'Великий кактус'},
        {'category': flowers, 'name': 'Кактус'},
        {'category': flowers, 'name': 'Гіпсофіла'},
        {'category': flowers, 'name': 'Бавовна'},
        {'category': flowers, 'name': 'Пшениця'},
        {'category': flowers, 'name': 'Лілії'},
        {'category': flowers, 'name': 'Тюльпани'},
        {'category': flowers, 'name': 'Фіалки'},
        {'category': flowers, 'name': 'Лаванда'},
        {'category': flowers, 'name': 'Орхідеї'},
        {'category': flowers, 'name': 'Хризантеми'},
        {'category': flowers, 'name': 'Іриси'},
        {'category': flowers, 'name': 'Соняшники'},
        {'category': flowers, 'name': 'Гербери'},
        {'category': flowers, 'name': 'Півонії'},
        {'category': flowers, 'name': 'Маки'},
        {'category': flowers, 'name': 'Волошки'},
        {'category': flowers, 'name': 'Ромашки'},
        {'category': flowers, 'name': 'Магнолії'},
        {'category': flowers, 'name': 'Амаріліси'},
        {'category': flowers, 'name': 'Гладіолуси'},
        {'category': flowers, 'name': 'Камелії'},
        {'category': flowers, 'name': 'Лілаки'},
        {'category': flowers, 'name': 'Нарциси'},
        {'category': flowers, 'name': 'Астри'},
        {'category': flowers, 'name': 'Клематиси'},
        {'category': flowers, 'name': 'Флокси'},
        {'category': flowers, 'name': 'Гвоздики'},
        {'category': flowers, 'name': 'Крокуси'},
        {'category': flowers, 'name': 'Тюберози'},
        {'category': flowers, 'name': 'Петунії'},
        {'category': flowers, 'name': 'Шипшина'},
        {'category': flowers, 'name': 'Шпориш'},
        {'category': flowers, 'name': 'Конвалії'},
        {'category': flowers, 'name': 'Папороть'},
        {'category': flowers, 'name': 'Лютики'},
        {'category': flowers, 'name': 'Мальви'},
        {'category': flowers, 'name': 'Фламінго'},
        {'category': flowers, 'name': 'Багатоцвіття'},
        {'category': flowers, 'name': 'Ліловий лотос'},
        {'category': flowers, 'name': 'Бамбуковий пагін'},
        {'category': flowers, 'name': 'Азалії'},
        {'category': flowers, 'name': 'Василеки'},
        {'category': flowers, 'name': 'Листя акації'},
        {'category': flowers, 'name': 'Черешневий цвіт'},
        {'category': flowers, 'name': 'Кульбаби'},

        # Id 51 - 65
        {'category': packing, 'name': 'Фіолетова обгортка'},
        {'category': packing, 'name': 'Синя смужка'},
        {'category': packing, 'name': 'Червона смужка'},
        {'category': packing, 'name': 'Біла обгортка'},
        {'category': packing, 'name': 'Прозора обгортка'},
        {'category': packing, 'name': 'Зелена обгортка'},
        {'category': packing, 'name': 'Золотиста смужка'},
        {'category': packing, 'name': 'Срібна обгортка'},
        {'category': packing, 'name': 'Рожева смужка'},
        {'category': packing, 'name': 'Брунатна обгортка'},
        {'category': packing, 'name': 'Жовта смужка'},
        {'category': packing, 'name': 'Чорна обгортка'},
        {'category': packing, 'name': 'Помаранчева смужка'},
        {'category': packing, 'name': 'Світло-сіра обгортка'},
        {'category': packing, 'name': 'Темно-сіра смужка'},

        # Id 66 - 80
        {'category': toys, 'name': 'Рожевий заєць'},
        {'category': toys, 'name': 'Маленький медвідь'},
        {'category': toys, 'name': 'Великий медвідь'},
        {'category': toys, 'name': 'Медвідь з сердечком'},
        {'category': toys, 'name': 'Плюшовий кролик'},
        {'category': toys, 'name': 'Жираф-плюш'},
        {'category': toys, 'name': 'М\'яч для гри'},
        {'category': toys, 'name': 'Дерев\'яна лялька'},
        {'category': toys, 'name': 'Автомобіль-іграшка'},
        {'category': toys, 'name': 'Пазли для дітей'},
        {'category': toys, 'name': 'М\'яка лисичка'},
        {'category': toys, 'name': 'Іграшковий вертоліт'},
        {'category': toys, 'name': 'Кубики для будівництва'},
        {'category': toys, 'name': 'Кольоровий коврик-гра'},
        {'category': toys, 'name': 'М\'ячик для котика'},
    ]

    db.session.query(Goods).delete()
    db.session.execute(text(f"ALTER SEQUENCE goods_id_seq RESTART WITH 1"))

    for data in goods_data:
        category = Goods(**data)
        db.session.add(category)

    db.session.commit()


def add_suppliers():
    suppliers_data = [
        {'name': 'Антон', 'contactInfo': '+380 22 222 2222', 'additional': 'Не пунктуальний'},
        {'name': 'Іван', 'contactInfo': 'ivan@example.com', 'additional': 'Доставка по місту'},
        {'name': 'Марія', 'contactInfo': '+380 99 999 9999', 'additional': 'Розташовується на площі'},

        {'name': 'Василь', 'contactInfo': 'vasya@example.com', 'additional': 'Білий спрінтер'},
        {'name': 'Коля', 'contactInfo': 'kolya@example.com', 'additional': 'Грубіян'},

        {'name': 'Олег', 'contactInfo': 'toysShop@example.com', 'additional': 'Велика, рожева фура'},
    ]

    db.session.query(Suppliers).delete()
    db.session.execute(text("ALTER SEQUENCE suppliers_id_seq RESTART WITH 1"))

    for data in suppliers_data:
        supplier = Suppliers(**data)
        db.session.add(supplier)

    db.session.commit()


def add_expenses():
    supplier_1 = Suppliers.query.filter_by(id=1).first()
    supplier_2 = Suppliers.query.filter_by(id=2).first()
    supplier_3 = Suppliers.query.filter_by(id=3).first()

    supplier_4 = Suppliers.query.filter_by(id=4).first()

    supplier_5 = Suppliers.query.filter_by(id=5).first()

    flowers = Categories.query.filter_by(id=1).first()
    packing = Categories.query.filter_by(id=2).first()
    toys = Categories.query.filter_by(id=3).first()

    expenses_data = [
        {'date': "2024-02-01", 'supplier': supplier_1, 'category': flowers, 'total': 0},
        {'date': "2024-02-01", 'supplier': supplier_4, 'category': packing, 'total': 0},
        {'date': "2024-02-02", 'supplier': supplier_4, 'category': packing, 'total': 0},
        {'date': "2024-02-03", 'supplier': supplier_2, 'category': flowers, 'total': 0},
        {'date': "2024-02-03", 'supplier': supplier_5, 'category': toys, 'total': 0},
        {'date': "2024-02-03", 'supplier': supplier_2, 'category': flowers, 'total': 0},
        {'date': "2024-02-06", 'supplier': supplier_2, 'category': flowers, 'total': 0},
        {'date': "2024-02-08", 'supplier': supplier_5, 'category': toys, 'total': 0},
        {'date': "2024-02-10", 'supplier': supplier_2, 'category': flowers, 'total': 0},
        {'date': "2024-02-12", 'supplier': supplier_5, 'category': toys, 'total': 0},
        {'date': "2024-02-16", 'supplier': supplier_1, 'category': flowers, 'total': 0},
        {'date': "2024-02-17", 'supplier': supplier_5, 'category': toys, 'total': 0},
        {'date': "2024-02-18", 'supplier': supplier_3, 'category': flowers, 'total': 0},
        {'date': "2024-02-19", 'supplier': supplier_4, 'category': packing, 'total': 0},
        {'date': "2024-02-19", 'supplier': supplier_5, 'category': toys, 'total': 0},
        {'date': "2024-02-20", 'supplier': supplier_5, 'category': toys, 'total': 0},
        {'date': "2024-02-24", 'supplier': supplier_2, 'category': flowers, 'total': 0},
        {'date': "2024-02-24", 'supplier': supplier_4, 'category': packing, 'total': 0},
        {'date': "2024-02-25", 'supplier': supplier_3, 'category': flowers, 'total': 0},
        {'date': "2024-02-27", 'supplier': supplier_1, 'category': flowers, 'total': 0},
        {'date': "2024-02-28", 'supplier': supplier_4, 'category': packing, 'total': 0},
        {'date': "2024-02-29", 'supplier': supplier_1, 'category': flowers, 'total': 0},
        {'date': "2024-03-01", 'supplier': supplier_2, 'category': flowers, 'total': 0},
        {'date': "2024-03-02", 'supplier': supplier_4, 'category': packing, 'total': 0},
        {'date': "2024-03-03", 'supplier': supplier_4, 'category': packing, 'total': 0},
        {'date': "2024-03-03", 'supplier': supplier_2, 'category': flowers, 'total': 0},
        {'date': "2024-03-05", 'supplier': supplier_5, 'category': toys, 'total': 0},
        {'date': "2024-03-06", 'supplier': supplier_1, 'category': flowers, 'total': 0},
        {'date': "2024-03-06", 'supplier': supplier_5, 'category': toys, 'total': 0},
        {'date': "2024-03-07", 'supplier': supplier_4, 'category': packing, 'total': 0},
    ]

    db.session.query(Expenses).delete()
    db.session.execute(text("ALTER SEQUENCE expenses_id_seq RESTART WITH 1"))

    for data in expenses_data:
        expense = Expenses(**data)
        db.session.add(expense)

    db.session.commit()


def add_expenses_elms():
    expenses_elms_data = []

    db.session.query(ExpensesElements).delete()
    db.session.execute(text("ALTER SEQUENCE expenses_elements_id_seq RESTART WITH 1"))

    for expense in range(1, 11):
        used_elements = []
        expense_total = 0

        for element in range(5, 15):
            element_id = random.randint(1, 50)
            if element_id not in used_elements:
                quantity = random.randint(1, 15)
                price = random.randint(10, 25)
                expense_total += quantity * price

                used_elements.append(element_id)
                expenses_elms_data.append(
                    {'expense': Expenses.query.filter_by(id=expense).first(),
                     'product': Goods.query.filter_by(id=element_id).first(),
                     'quantity': quantity,
                     'price': price},
                )

        expense_object = Expenses.query.filter_by(id=expense).first()
        expense_object.total = expense_total
        db.session.add(expense_object)
    for expense in range(21, 26):
        used_elements = []
        expense_total = 0

        for element in range(5, 15):
            element_id = random.randint(1, 50)
            if element_id not in used_elements:
                quantity = random.randint(1, 15)
                price = random.randint(10, 25)
                expense_total += quantity * price

                used_elements.append(element_id)
                expenses_elms_data.append(
                    {'expense': Expenses.query.filter_by(id=expense).first(),
                     'product': Goods.query.filter_by(id=element_id).first(),
                     'quantity': quantity,
                     'price': price},
                )

        expense_object = Expenses.query.filter_by(id=expense).first()
        expense_object.total = expense_total
        db.session.add(expense_object)

    for expense in range(11, 16):
        used_elements = []
        expense_total = 0

        for element in range(5, 8):
            element_id = random.randint(51, 65)
            if element_id not in used_elements:
                quantity = random.randint(1, 7)
                price = random.randint(10, 15)
                expense_total += quantity * price

                used_elements.append(element_id)
                expenses_elms_data.append(
                    {'expense': Expenses.query.filter_by(id=expense).first(),
                     'product': Goods.query.filter_by(id=element_id).first(),
                     'quantity': quantity,
                     'price': price},
                )

        expense_object = Expenses.query.filter_by(id=expense).first()
        expense_object.total = expense_total
        db.session.add(expense_object)
    for expense in range(26, 29):
        used_elements = []
        expense_total = 0

        for element in range(5, 8):
            element_id = random.randint(51, 65)
            if element_id not in used_elements:
                quantity = random.randint(1, 7)
                price = random.randint(10, 15)
                expense_total += quantity * price

                used_elements.append(element_id)
                expenses_elms_data.append(
                    {'expense': Expenses.query.filter_by(id=expense).first(),
                     'product': Goods.query.filter_by(id=element_id).first(),
                     'quantity': quantity,
                     'price': price},
                )

        expense_object = Expenses.query.filter_by(id=expense).first()
        expense_object.total = expense_total
        db.session.add(expense_object)

    for expense in range(16, 21):
        used_elements = []
        expense_total = 0

        for element in range(3, 6):
            element_id = random.randint(66, 80)
            if element_id not in used_elements:
                quantity = random.randint(1, 8)
                price = random.randint(10, 16)
                expense_total += quantity * price

                used_elements.append(element_id)
                expenses_elms_data.append(
                    {'expense': Expenses.query.filter_by(id=expense).first(),
                     'product': Goods.query.filter_by(id=element_id).first(),
                     'quantity': quantity,
                     'price': price},
                )

        expense_object = Expenses.query.filter_by(id=expense).first()
        expense_object.total = expense_total
        db.session.add(expense_object)
    for expense in range(29, 31):
        used_elements = []
        expense_total = 0

        for element in range(3, 6):
            element_id = random.randint(66, 80)
            if element_id not in used_elements:
                quantity = random.randint(1, 8)
                price = random.randint(10, 16)
                expense_total += quantity * price

                used_elements.append(element_id)
                expenses_elms_data.append(
                    {'expense': Expenses.query.filter_by(id=expense).first(),
                     'product': Goods.query.filter_by(id=element_id).first(),
                     'quantity': quantity,
                     'price': price},
                )

        expense_object = Expenses.query.filter_by(id=expense).first()
        expense_object.total = expense_total
        db.session.add(expense_object)
    db.session.commit()

    for data in expenses_elms_data:
        element = ExpensesElements(**data)
        db.session.add(element)

    db.session.commit()


def add_orders():
    orders_data = [
        # Id 1-10
        {'date': '2024-02-01', 'status': 'Продано', 'price': 0, 'discount': 0},
        {'date': '2024-02-03', 'status': 'Продано', 'price': 0, 'discount': 0},
        {'date': '2024-02-06', 'status': 'Продано', 'price': 0, 'discount': 0},

        {'date': '2024-03-12', 'status': 'Списано', 'price': 0, 'discount': 0},
        {'date': '2024-03-11', 'status': 'Продано', 'price': 0, 'discount': 0},
        {'date': '2024-03-14', 'status': 'Списано', 'price': 0, 'discount': 0},
        {'date': '2024-03-15', 'status': 'Списано', 'price': 0, 'discount': 0},
        {'date': '2024-03-19', 'status': 'Продано', 'price': 0, 'discount': 0},

        {'date': '2024-03-20', 'status': 'Продано', 'price': 0, 'discount': 0},
        {'date': '2024-03-21', 'status': 'Списано', 'price': 0, 'discount': 0},
    ]

    db.session.query(Orders).delete()
    db.session.execute(text("ALTER SEQUENCE orders_id_seq RESTART WITH 1"))

    for data in orders_data:
        order = Orders(**data)
        db.session.add(order)

    db.session.commit()


def add_orders_elements():
    order_elements = []

    db.session.query(OrdersElements).delete()
    db.session.execute(text("ALTER SEQUENCE orders_elements_id_seq RESTART WITH 1"))

    for order in Orders.query.all():
        total = 0
        flowers = ExpensesElements.query.filter_by(expense=Expenses.query.filter_by(id=order.id).first()).all()
        existing_flowers = []
        for flower in flowers:
            if flower.id not in existing_flowers:
                new_order_element = OrdersElements(order=order, product=flower.product, quantity=flower.quantity,
                                                   price=flower.price * 2.20)
                db.session.add(new_order_element)
                existing_flowers.append(flower.id)
                total += flower.quantity * flower.price * 2.20
        if order.id % 2 == 0:
            packing_elements = ExpensesElements.query.filter_by(expense=Expenses.query.filter_by(id=10 + order.id // 2).first()).all()
            existing_packing = []
            for packing in packing_elements:
                if packing.id not in existing_packing:
                    new_order_element = OrdersElements(order=order, product=packing.product, quantity=packing.quantity,
                                                       price=packing.price * 2.20)
                    db.session.add(new_order_element)
                    existing_packing.append(packing.id)
                    total += packing.quantity * packing.price * 2.20
        else:
            toys = ExpensesElements.query.filter_by(expense=Expenses.query.filter_by(id=16 + order.id).first()).all()
            existing_toys = []
            for toy in toys:
                if toy.id not in existing_toys:
                    new_order_element = OrdersElements(order=order, product=toy.product, quantity=toy.quantity,
                                                       price=toy.price * 2.20)
                    db.session.add(new_order_element)
                    existing_toys.append(toy.id)
                    total += toy.quantity * toy.price * 2.20

        order.price = round(total)
        db.session.commit()

    for data in order_elements:
        order_element = OrdersElements(**data)
        db.session.add(order_element)

    db.session.commit()


with app.app_context():
    db.drop_all()
    db.create_all()
    add_categories()
    add_goods()
    add_suppliers()
    add_expenses()
    add_expenses_elms()
    add_orders()
    add_orders_elements()
