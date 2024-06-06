import random
import argparse
from progress.bar import ChargingBar
from datetime import datetime, timedelta
from src import db, app
from sqlalchemy import text
from src.models.goods import Goods, Categories
from src.models.suppliers import Suppliers
from src.models.expenses import Expenses, ExpensesElements
from src.models.orders import Orders, OrdersElements
from src.utils.settings import util_reset_settings

# Argument Parser
parser = argparse.ArgumentParser(description='Process some dates.')
parser.add_argument('--years', type=int, default=0, help='number of years to subtract from the current year')
parser.add_argument('--months', type=int, default=0, help='number of months to subtract from the current month')
parser.add_argument('--days', type=int, default=0, help='number of days to subtract from the current day')
args = parser.parse_args()

starting_date = None
today = datetime.today()
year = args.years
months = args.months
days = args.days


if year == 0 and months == 0 and days == 0:
    starting_date = today.replace(month=1, day=1)
else:
    target_year = today.year - year
    target_month = today.month - months
    if target_month <= 0:
        target_year -= 1
        target_month += 12
    starting_date = today.replace(year=target_year, month=target_month, day=1) - timedelta(days=days)
    starting_date = starting_date

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
    flowers = Categories.query.filter_by(name='Квіти').first()
    packing = Categories.query.filter_by(name='Упаковка').first()
    toys = Categories.query.filter_by(name='Іграшки').first()

    goods_data = [
        {'category': flowers, 'name': 'Білі троянди'},
        {'category': flowers, 'name': 'Червоні троянди'},
        {'category': flowers, 'name': 'Рожеві троянди'},
        {'category': flowers, 'name': 'Фіолетові троянди'},
        {'category': flowers, 'name': 'Кактус'},
        {'category': flowers, 'name': 'Гіпсофіла'},
        {'category': flowers, 'name': 'Бавовна'},
        {'category': flowers, 'name': 'Лілії'},
        {'category': flowers, 'name': 'Тюльпани'},
        {'category': flowers, 'name': 'Фіалки'},
        {'category': flowers, 'name': 'Лаванда'},
        {'category': flowers, 'name': 'Орхідеї'},
        {'category': flowers, 'name': 'Хризантеми'},
        {'category': flowers, 'name': 'Іриси'},
        {'category': flowers, 'name': 'Півонії'},
        {'category': flowers, 'name': 'Маки'},
        {'category': flowers, 'name': 'Ромашки'},
        {'category': flowers, 'name': 'Амаріліси'},
        {'category': flowers, 'name': 'Нарциси'},
        {'category': flowers, 'name': 'Гвоздики'},
        {'category': packing, 'name': 'Біла обгортка'},
        {'category': packing, 'name': 'Прозора обгортка'},
        {'category': packing, 'name': 'Зелена обгортка'},
        {'category': packing, 'name': 'Срібна обгортка'},
        {'category': packing, 'name': 'Чорна обгортка'},
        {'category': packing, 'name': 'Рожева смужка'},
        {'category': packing, 'name': 'Синя смужка'},
        {'category': packing, 'name': 'Червона смужка'},
        {'category': packing, 'name': 'Жовта смужка'},
        {'category': packing, 'name': 'Помаранчева смужка'},
        {'category': toys, 'name': 'Рожевий заєць'},
        {'category': toys, 'name': 'Маленький медвідь'},
        {'category': toys, 'name': 'Великий медвідь'},
        {'category': toys, 'name': 'Плюшовий кролик'},
        {'category': toys, 'name': 'Жираф-плюш'},
        {'category': toys, 'name': 'Дерев\'яна лялька'},
        {'category': toys, 'name': 'Машинка'},
        {'category': toys, 'name': 'М\'яка лисичка'},
        {'category': toys, 'name': 'Іграшковий вертоліт'},
        {'category': toys, 'name': 'Кубики'},
    ]

    db.session.query(Goods).delete()
    db.session.execute(text(f"ALTER SEQUENCE goods_id_seq RESTART WITH 1"))

    for data in goods_data:
        good = Goods(**data)
        db.session.add(good)

    db.session.commit()

def add_suppliers():
    suppliers_data = [
        {'name': 'Антон', 'contactInfo': '+380 22 222 2222', 'additional': 'Не пунктуальний'},
        {'name': 'Іван', 'contactInfo': 'ivan@example.com', 'additional': 'Доставка по місту'},
        {'name': 'Марія', 'contactInfo': '+380 99 999 9999', 'additional': 'Розташовується на площі'},
        {'name': 'Василь', 'contactInfo': 'vasya@example.com', 'additional': 'Білий спрінтер'},
        {'name': 'Коля', 'contactInfo': 'kolya@example.com', 'additional': 'Грубіян'},
        {'name': 'Олег', 'contactInfo': 'shop@example.com', 'additional': 'Велика, рожева фура'},
    ]

    db.session.query(Suppliers).delete()
    db.session.execute(text("ALTER SEQUENCE suppliers_id_seq RESTART WITH 1"))

    for data in suppliers_data:
        supplier = Suppliers(**data)
        db.session.add(supplier)

    db.session.commit()

def add_expenses():
    suppliers = Suppliers.query.all()
    categories = Categories.query.all()

    expenses_data = []
    current_day = starting_date
    expense_probability = 60
    while current_day <= today:
        chance = random.randint(0, 100)
        if chance <= expense_probability:
            expenses_data.append({
                'date': current_day, 'supplier': random.choice(suppliers), 'category': random.choice(categories), 'total': 0
            })
        current_day += timedelta(days=1)

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

    bar = ChargingBar(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]   Filling expenses", max=len(Expenses.query.all()), suffix="%(index)d/%(max)d")
    for category in Categories.query.all():
        available_goods = Goods.query.filter_by(category=category).all()
        expenses = Expenses.query.filter_by(category=category).all()
        for expense in expenses:
            bar.next()
            used_elements = []
            expense_total = 0
            elements_quantity = range(1, 6)

            for element in elements_quantity:
                element = random.randint(0, len(available_goods)-1)
                if element not in used_elements:
                    used_elements.append(element)

                    quantity = random.randint(1, 13)
                    price = random.randint(10, 25)
                    expense_total += quantity * price

                    expenses_elms_data.append(
                        {'expense': expense,
                         'product': available_goods[element],
                         'quantity': quantity,
                         'price': price},
                    )
            expense.total = expense_total
            db.session.add(expense)
    bar.finish()
    db.session.commit()

    for data in expenses_elms_data:
        element = ExpensesElements(**data)
        db.session.add(element)

    db.session.commit()

def add_orders():
    statuses = ["Продано", "Списано", "Вітрина"]
    orders_data = []

    current_day = starting_date
    order_probability = 60
    while current_day <= today:
        chance = random.randint(0, 100)
        if chance <= order_probability:
            orders_data.append({
                'date': current_day, 'status': random.choices(statuses, weights=(75, 20, 5), k=1)[0], 'price': 0, 'discount': 0
            })
        current_day += timedelta(days=1)

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
    orders = Orders.query.all()
    bar = ChargingBar(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]   Filling orders", max=len(Orders.query.all()), suffix="%(index)d/%(max)d")
    for order in orders:
        bar.next()
        categories = Categories.query.all()
        order_categories = random.sample(categories, random.randint(1, len(categories)))
        used_elements = []
        elements_limit = 5
        price = 0

        for category in order_categories:
            available_goods = ExpensesElements.query.join(ExpensesElements.product).filter(Goods.category == category).all()
            elements_quantity = range(3, 5)

            if len(used_elements) >= elements_limit:
                break
            if len(available_goods) == 0:
                continue

            for element in elements_quantity:
                element = available_goods[random.randint(0, len(available_goods)-1)]
                if element.product not in used_elements:
                    instock_quantity = (
                        sum(elem.quantity for elem in available_goods if elem.product == element.product) -
                        sum(elem['quantity'] for elem in order_elements if elem['product'] == element.product)
                    )
                    if instock_quantity == 0:
                        continue
                    used_elements.append(element.product)

                    quantity = random.randint(1, min(instock_quantity, 10))
                    element_price = random.randint(10, 25) * 2.20
                    price += quantity * element_price

                    order_elements.append({
                        'order': order,
                        'product': element.product,
                        'quantity': quantity,
                        'price': element_price,
                    })
        if len(used_elements) == 0:
            db.session.delete(order)
            db.session.commit()
        else:
            order.price = round(price)
            db.session.add(order)
    bar.finish()

    for data in order_elements:
        order_element = OrdersElements(**data)
        db.session.add(order_element)

    db.session.commit()

with app.app_context():
    time_started = datetime.now()
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Generating data from {starting_date.strftime('%Y-%m-%d')}")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]  Dropping db")
    db.drop_all()
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]  Creating db")
    db.create_all()

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]  Resetting settings")
    util_reset_settings()
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]  Adding categories")
    add_categories()
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]  Adding goods")
    add_goods()
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]  Adding suppliers")
    add_suppliers()
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]  Adding expenses")
    add_expenses()
    add_expenses_elms()
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]  Adding orders")
    add_orders()
    add_orders_elements()
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Done in {datetime.now() - time_started}")
