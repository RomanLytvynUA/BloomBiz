import random
import argparse
from progress.bar import ChargingBar
from datetime import datetime, timedelta
from src import db, app
from sqlalchemy import text
from src.models.auth import RegistrationCode, User
from src.models.goods import Goods, Categories
from src.models.suppliers import Suppliers
from src.models.expenses import Expenses, ExpensesElements
from src.models.orders import Orders, OrdersElements
from src.models.customers import Customers
from src.utils.settings import util_reset_settings

# Argument Parser
parser = argparse.ArgumentParser(description="Process some dates.")
parser.add_argument(
    "--years",
    type=int,
    default=0,
    help="number of years to subtract from the current year",
)
parser.add_argument(
    "--lang",
    type=str,
    choices=["ukr", "eng"],
    default="eng",
    help="language of fake data to be generated (ukr/eng)",
)
parser.add_argument(
    "--months",
    type=int,
    default=0,
    help="number of months to subtract from the current month",
)
parser.add_argument(
    "--days",
    type=int,
    default=0,
    help="number of days to subtract from the current day",
)
args = parser.parse_args()

starting_date = None
today = datetime.today()
year = args.years
months = args.months
days = args.days
lang = args.lang


if year == 0 and months == 0 and days == 0:
    # set starting_date to first day of current year by default
    starting_date = today.replace(month=1, day=1)
else:
    # set starting_date based on offset provided
    target_year = today.year - year
    target_month = today.month - months
    if target_month <= 0:
        target_year -= 1
        target_month += 12
    starting_date = today.replace(
        year=target_year, month=target_month, day=1
    ) - timedelta(days=days)
    starting_date = starting_date


def add_user():
    db.session.query(User).delete()
    db.session.execute(text(f"ALTER SEQUENCE user_id_seq RESTART WITH 1"))

    new_user = User(username="User", password="Qwerty123")

    db.session.add(new_user)
    db.session.commit()


def add_reg_code():
    db.session.query(RegistrationCode).delete()
    db.session.execute(text(f"ALTER SEQUENCE registration_code_id_seq RESTART WITH 1"))

    new_code = RegistrationCode(code="AA1111AAA")

    db.session.add(new_code)
    db.session.commit()


def add_categories():
    categories_data = (
        [
            {"name": "Квіти", "units": "шт."},
            {"name": "Упаковка", "units": "м."},
            {"name": "Іграшки", "units": "шт."},
        ]
        if lang == "ukr"
        else [
            {"name": "Flowers", "units": "pcs."},
            {"name": "Packing", "units": "m."},
            {"name": "Toys", "units": "pcs."},
        ]
    )

    db.session.query(Categories).delete()
    db.session.execute(text(f"ALTER SEQUENCE categories_id_seq RESTART WITH 1"))

    for data in categories_data:
        category = Categories(**data)
        db.session.add(category)

    db.session.commit()


def add_goods():
    flowers = (
        Categories.query.filter_by(name="Квіти").first()
        if lang == "ukr"
        else Categories.query.filter_by(name="Flowers").first()
    )
    packing = (
        Categories.query.filter_by(name="Упаковка").first()
        if lang == "ukr"
        else Categories.query.filter_by(name="Packing").first()
    )
    toys = (
        Categories.query.filter_by(name="Іграшки").first()
        if lang == "ukr"
        else Categories.query.filter_by(name="Toys").first()
    )

    goods_data = (
        [
            {"category": flowers, "name": "Білі троянди"},
            {"category": flowers, "name": "Червоні троянди"},
            {"category": flowers, "name": "Рожеві троянди"},
            {"category": flowers, "name": "Фіолетові троянди"},
            {"category": flowers, "name": "Кактус"},
            {"category": flowers, "name": "Гіпсофіла"},
            {"category": flowers, "name": "Бавовна"},
            {"category": flowers, "name": "Лілії"},
            {"category": flowers, "name": "Тюльпани"},
            {"category": flowers, "name": "Фіалки"},
            {"category": flowers, "name": "Лаванда"},
            {"category": flowers, "name": "Орхідеї"},
            {"category": flowers, "name": "Хризантеми"},
            {"category": flowers, "name": "Іриси"},
            {"category": flowers, "name": "Півонії"},
            {"category": flowers, "name": "Маки"},
            {"category": flowers, "name": "Ромашки"},
            {"category": flowers, "name": "Амаріліси"},
            {"category": flowers, "name": "Нарциси"},
            {"category": flowers, "name": "Гвоздики"},
            {"category": packing, "name": "Біла обгортка"},
            {"category": packing, "name": "Прозора обгортка"},
            {"category": packing, "name": "Зелена обгортка"},
            {"category": packing, "name": "Срібна обгортка"},
            {"category": packing, "name": "Чорна обгортка"},
            {"category": packing, "name": "Рожева смужка"},
            {"category": packing, "name": "Синя смужка"},
            {"category": packing, "name": "Червона смужка"},
            {"category": packing, "name": "Жовта смужка"},
            {"category": packing, "name": "Помаранчева смужка"},
            {"category": toys, "name": "Рожевий заєць"},
            {"category": toys, "name": "Маленький медвідь"},
            {"category": toys, "name": "Великий медвідь"},
            {"category": toys, "name": "Плюшовий кролик"},
            {"category": toys, "name": "Жираф-плюш"},
            {"category": toys, "name": "Дерев'яна лялька"},
            {"category": toys, "name": "Машинка"},
            {"category": toys, "name": "М'яка лисичка"},
            {"category": toys, "name": "Іграшковий вертоліт"},
            {"category": toys, "name": "Кубики"},
        ]
        if lang == "ukr"
        else [
            {"category": flowers, "name": "White Roses"},
            {"category": flowers, "name": "Red Roses"},
            {"category": flowers, "name": "Pink Roses"},
            {"category": flowers, "name": "Purple Roses"},
            {"category": flowers, "name": "Cactus"},
            {"category": flowers, "name": "Gypsophila"},
            {"category": flowers, "name": "Cotton"},
            {"category": flowers, "name": "Lilies"},
            {"category": flowers, "name": "Tulips"},
            {"category": flowers, "name": "Violets"},
            {"category": flowers, "name": "Lavender"},
            {"category": flowers, "name": "Orchids"},
            {"category": flowers, "name": "Chrysanthemums"},
            {"category": flowers, "name": "Irises"},
            {"category": flowers, "name": "Peonies"},
            {"category": flowers, "name": "Poppies"},
            {"category": flowers, "name": "Daisies"},
            {"category": flowers, "name": "Amaryllis"},
            {"category": flowers, "name": "Daffodils"},
            {"category": flowers, "name": "Carnations"},
            {"category": packing, "name": "White Wrap"},
            {"category": packing, "name": "Transparent Wrap"},
            {"category": packing, "name": "Green Wrap"},
            {"category": packing, "name": "Silver Wrap"},
            {"category": packing, "name": "Black Wrap"},
            {"category": packing, "name": "Pink Ribbon"},
            {"category": packing, "name": "Blue Ribbon"},
            {"category": packing, "name": "Red Ribbon"},
            {"category": packing, "name": "Yellow Ribbon"},
            {"category": packing, "name": "Orange Ribbon"},
            {"category": toys, "name": "Pink Bunny"},
            {"category": toys, "name": "Small Bear"},
            {"category": toys, "name": "Large Bear"},
            {"category": toys, "name": "Plush Rabbit"},
            {"category": toys, "name": "Plush Giraffe"},
            {"category": toys, "name": "Wooden Doll"},
            {"category": toys, "name": "Toy Car"},
            {"category": toys, "name": "Soft Fox"},
            {"category": toys, "name": "Toy Helicopter"},
            {"category": toys, "name": "Blocks"},
        ]
    )

    db.session.query(Goods).delete()
    db.session.execute(text(f"ALTER SEQUENCE goods_id_seq RESTART WITH 1"))

    for data in goods_data:
        good = Goods(**data)
        db.session.add(good)

    db.session.commit()


def add_suppliers():
    suppliers_data = (
        [
            {
                "name": "Антон",
                "contactInfo": "+380 22 222 2222",
                "additional": "Не пунктуальний",
            },
            {
                "name": "Іван",
                "contactInfo": "ivan@example.com",
                "additional": "Доставка по місту",
            },
            {
                "name": "Марія",
                "contactInfo": "+380 99 999 9999",
                "additional": "Розташовується на площі",
            },
            {
                "name": "Василь",
                "contactInfo": "vasya@example.com",
                "additional": "Білий спрінтер",
            },
            {
                "name": "Коля",
                "contactInfo": "kolya@example.com",
                "additional": "Грубіян",
            },
            {
                "name": "Олег",
                "contactInfo": "shop@example.com",
                "additional": "Велика, рожева фура",
            },
        ]
        if lang == "ukr"
        else [
            {
                "name": "Anton",
                "contactInfo": "+1 555-555-5555",
                "additional": "Not punctual",
            },
            {
                "name": "John",
                "contactInfo": "john@example.com",
                "additional": "City-wide delivery",
            },
            {
                "name": "Mary",
                "contactInfo": "+1 555-555-9999",
                "additional": "Located in the town square",
            },
            {
                "name": "William",
                "contactInfo": "will@example.com",
                "additional": "White Sprinter van",
            },
            {
                "name": "Nick",
                "contactInfo": "nick@example.com",
                "additional": "Rude",
            },
            {
                "name": "Oliver",
                "contactInfo": "shop@example.com",
                "additional": "Large, pink truck",
            },
        ]
    )

    db.session.query(Suppliers).delete()
    db.session.execute(text("ALTER SEQUENCE suppliers_id_seq RESTART WITH 1"))

    for data in suppliers_data:
        supplier = Suppliers(**data)
        db.session.add(supplier)

    db.session.commit()


def add_customers():
    customers_data = (
        [
            {
                "name": "Антон",
                "contactInfo": "+380 11 123 4567",
                "additional": "Не пунктуальний",
            },
            {
                "name": "Олександр Миколайович",
                "contactInfo": "+380 12 234 5678",
                "additional": "Ввічливий",
            },
            {
                "name": "Марія Коваленко",
                "contactInfo": "+380 13 345 6789",
                "additional": "Любить каву",
            },
            {
                "name": "Віктор",
                "contactInfo": "+380 14 456 7890",
                "additional": "Не любить чекати",
            },
            {
                "name": "Катерина Олексіївна",
                "contactInfo": "+380 15 567 8901",
                "additional": "Завжди посміхається",
            },
            {
                "name": "Іван Петров",
                "contactInfo": "+380 16 678 9012",
                "additional": "Вегетаріанець",
            },
            {
                "name": "Наталія",
                "contactInfo": "+380 17 789 0123",
                "additional": "Любить подорожувати",
            },
            {
                "name": "Андрій Мельник",
                "contactInfo": "+380 18 890 1234",
                "additional": "Завжди пунктуальний",
            },
            {
                "name": "Юлія",
                "contactInfo": "+380 19 901 2345",
                "additional": "Має кота",
            },
            {
                "name": "Дмитро",
                "contactInfo": "+380 20 012 3456",
                "additional": "Не любить дощ",
            },
            {
                "name": "Олена Сердюк",
                "contactInfo": "+380 21 123 4567",
                "additional": "Любить читати",
            },
            {
                "name": "Сергій",
                "contactInfo": "+380 22 234 5678",
                "additional": "Любить спорт",
            },
            {
                "name": "Валентина Іванівна",
                "contactInfo": "+380 23 345 6789",
                "additional": "Колекціонує марки",
            },
            {
                "name": "Богдан",
                "contactInfo": "+380 24 456 7890",
                "additional": "Гарний кухар",
            },
            {
                "name": "Світлана",
                "contactInfo": "+380 25 567 8901",
                "additional": "Любить танцювати",
            },
            {
                "name": "Михайло",
                "contactInfo": "+380 26 678 9012",
                "additional": "Любить риболовлю",
            },
            {
                "name": "Ірина Павленко",
                "contactInfo": "+380 27 789 0123",
                "additional": "Не любить солодощів",
            },
            {
                "name": "Юрій",
                "contactInfo": "+380 28 890 1234",
                "additional": "Пише вірші",
            },
            {
                "name": "Тетяна Ростиславівна",
                "contactInfo": "+380 29 901 2345",
                "additional": "Має трьох дітей",
            },
            {
                "name": "Ростислав",
                "contactInfo": "+380 30 012 3456",
                "additional": "Любить подорожі",
            },
            {
                "name": "Галина",
                "contactInfo": "+380 31 123 4567",
                "additional": "Любить квіти",
            },
            {
                "name": "Олег",
                "contactInfo": "+380 32 234 5678",
                "additional": "Має собаку",
            },
            {
                "name": "Людмила",
                "contactInfo": "+380 33 345 6789",
                "additional": "Майстриня по вишивці",
            },
            {
                "name": "Арсен Іванович",
                "contactInfo": "+380 34 456 7890",
                "additional": "Збирає гриби",
            },
            {
                "name": "Віра",
                "contactInfo": "+380 35 567 8901",
                "additional": "Любить кататися на велосипеді",
            },
        ]
        if lang == "ukr"
        else [
            {
                "name": "Anthony",
                "contactInfo": "+1 212-555-4567",
                "additional": "Not punctual",
            },
            {
                "name": "Alexander",
                "contactInfo": "+1 213-555-5678",
                "additional": "Polite",
            },
            {
                "name": "Maria Smith",
                "contactInfo": "+1 214-555-6789",
                "additional": "Loves coffee",
            },
            {
                "name": "Victor",
                "contactInfo": "+1 215-555-7890",
                "additional": "Doesn't like waiting",
            },
            {
                "name": "Katherine",
                "contactInfo": "+1 216-555-8901",
                "additional": "Always smiling",
            },
            {
                "name": "John Peterson",
                "contactInfo": "+1 217-555-9012",
                "additional": "Vegetarian",
            },
            {
                "name": "Natalie",
                "contactInfo": "+1 218-555-0123",
                "additional": "Loves traveling",
            },
            {
                "name": "Andrew Miller",
                "contactInfo": "+1 219-555-1234",
                "additional": "Always punctual",
            },
            {
                "name": "Julia",
                "contactInfo": "+1 220-555-2345",
                "additional": "Has a cat",
            },
            {
                "name": "Dmitry",
                "contactInfo": "+1 221-555-3456",
                "additional": "Dislikes rain",
            },
            {
                "name": "Helen Johnson",
                "contactInfo": "+1 222-555-4567",
                "additional": "Loves reading",
            },
            {
                "name": "Sergey",
                "contactInfo": "+1 223-555-5678",
                "additional": "Loves sports",
            },
            {
                "name": "Valentina",
                "contactInfo": "+1 224-555-6789",
                "additional": "Collects stamps",
            },
            {
                "name": "Bogdan",
                "contactInfo": "+1 225-555-7890",
                "additional": "Great cook",
            },
            {
                "name": "Svetlana",
                "contactInfo": "+1 226-555-8901",
                "additional": "Loves dancing",
            },
            {
                "name": "Michael",
                "contactInfo": "+1 227-555-9012",
                "additional": "Loves fishing",
            },
            {
                "name": "Irene Parker",
                "contactInfo": "+1 228-555-0123",
                "additional": "Dislikes sweets",
            },
            {
                "name": "George",
                "contactInfo": "+1 229-555-1234",
                "additional": "Writes poetry",
            },
            {
                "name": "Tanya",
                "contactInfo": "+1 230-555-2345",
                "additional": "Has three children",
            },
            {
                "name": "Ross",
                "contactInfo": "+1 231-555-3456",
                "additional": "Loves traveling",
            },
            {
                "name": "Gail",
                "contactInfo": "+1 232-555-4567",
                "additional": "Loves flowers",
            },
            {
                "name": "Oliver",
                "contactInfo": "+1 233-555-5678",
                "additional": "Has a dog",
            },
            {
                "name": "Lydia",
                "contactInfo": "+1 234-555-6789",
                "additional": "Embroidery master",
            },
            {
                "name": "Aaron Smith",
                "contactInfo": "+1 235-555-7890",
                "additional": "Collects mushrooms",
            },
            {
                "name": "Vera",
                "contactInfo": "+1 236-555-8901",
                "additional": "Loves biking",
            },
        ]
    )

    db.session.query(Customers).delete()
    db.session.execute(text("ALTER SEQUENCE customers_id_seq RESTART WITH 1"))

    for data in customers_data:
        customer = Customers(**data)
        db.session.add(customer)

    db.session.commit()


def add_expenses():
    suppliers = Suppliers.query.all()
    categories = Categories.query.all()

    #  delete old expenses
    db.session.query(Expenses).delete()
    db.session.execute(text("ALTER SEQUENCE expenses_id_seq RESTART WITH 1"))

    expenses_data = []

    # add new expenses
    current_day = starting_date
    expense_probability = 60
    while current_day <= today:
        if random.randint(0, 100) <= expense_probability:
            expenses_data.append(
                {
                    "date": current_day,
                    "supplier": random.choice(suppliers),
                    "category": random.choice(categories),
                    "total": 0,
                }
            )
        current_day += timedelta(days=1)

    # commit new expenses
    for data in expenses_data:
        expense = Expenses(**data)
        db.session.add(expense)
    db.session.commit()


def add_expenses_elms():
    expenses_elms_data = []

    # delete old elements
    db.session.query(ExpensesElements).delete()
    db.session.execute(text("ALTER SEQUENCE expenses_elements_id_seq RESTART WITH 1"))

    bar = ChargingBar(
        f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]   Filling expenses",
        max=len(Expenses.query.all()),
        suffix="%(index)d/%(max)d",
    )
    for category in Categories.query.all():
        expenses = Expenses.query.filter_by(category=category).all()
        for expense in expenses:
            bar.next()
            used_goods = []
            expense_total = 0

            # add from 1 to 5 elements
            for _ in range(1, 6):
                available_goods = [
                    product for product in category.goods if product not in used_goods
                ]
                if available_goods:
                    product = random.choice(available_goods)
                    used_goods.append(product)

                    quantity = random.randint(1, 13)
                    price = random.randint(10, 20)
                    expense_total += quantity * price

                    expenses_elms_data.append(
                        {
                            "expense": expense,
                            "product": product,
                            "quantity": quantity,
                            "price": price,
                        },
                    )
                else:
                    break
            expense.total = expense_total
            db.session.add(expense)

    for data in expenses_elms_data:
        element = ExpensesElements(**data)
        db.session.add(element)
    db.session.commit()

    bar.finish()


def add_orders():
    orders_data = []
    statuses = (
        ["Продано", "Списано", "Вітрина"]
        if lang == "ukr"
        else ["Sold", "Written off", "Showcase"]
    )
    addresses = (
        [
            "вул. Рьостер-Штрассе 8, Вальтроп",
            "вул. Хрещатик, 1",
            "вул. Сумська, 2",
            "вул. Дерибасівська, 3",
            "вул. Шевченка, 4",
            "вул. Велика Васильківська, 5",
            "вул. Галицька, 6",
            "вул. Рівна, 7",
            "вул. Франка, 8",
            "вул. Січових Стрільців, 9",
            "вул. Зелена, 10",
            "вул. Коцюбинського, 11",
            "вул. Володимирська, 12",
            "вул. Прорізна, 13",
            "вул. Борщагівська, 14",
            "вул. Антоновича, 15",
            "вул. Грушевського, 16",
            "вул. Дорошенка, 17",
            "вул. Лесі Українки, 18",
            "вул. Городоцька, 19",
            "вул. Бандери, 20",
            "вул. Личаківська, 21",
            "вул. Теліги, 22",
            "вул. Набережна, 23",
            "вул. Соборна, 24",
            "вул. Саксаганського, 25",
        ]
        if lang == "ukr"
        else [
            "123 Maple Street",
            "456 Oak Avenue",
            "789 Pine Lane",
            "101 Elm Street",
            "202 Birch Road",
            "303 Cedar Boulevard",
            "404 Spruce Drive",
            "505 Fir Circle",
            "606 Aspen Way",
            "707 Chestnut Court",
            "808 Redwood Terrace",
            "909 Poplar Street",
            "111 Willow Avenue",
            "222 Holly Lane",
            "333 Maplewood Drive",
            "444 Oakwood Street",
            "555 Pinecrest Road",
            "666 Elmwood Drive",
            "777 Birch Lane",
            "888 Cedar Street",
            "999 Spruce Avenue",
            "1010 Fir Street",
            "1212 Aspen Court",
            "1313 Chestnut Drive",
            "1414 Redwood Road",
            "1515 Poplar Lane",
        ]
    )

    # delete old orders
    db.session.query(Orders).delete()
    db.session.execute(text("ALTER SEQUENCE orders_id_seq RESTART WITH 1"))

    # add new orders
    current_day = starting_date
    order_probability = 70
    customer_probability = 70
    receiver_probability = 30
    while current_day <= today:
        if random.randint(0, 100) <= order_probability:
            customer_id = None
            receiver_id = None
            address = ""
            if random.randint(0, 100) <= customer_probability:
                customer_id = random.randint(1, len(Customers.query.all()))
                if random.randint(0, 100) <= receiver_probability:
                    address = random.choice(addresses)
                    receiver_id = random.randint(1, len(Customers.query.all()))
                else:
                    receiver_id = customer_id

            orders_data.append(
                {
                    "date": current_day,
                    "status": random.choices(statuses, weights=(75, 20, 5), k=1)[0],
                    "price": 0,
                    "discount": 0,
                    "customer_id": customer_id,
                    "receiver_id": receiver_id,
                    "customer_address": address,
                }
            )
        current_day += timedelta(days=1)

    # commit new orders
    for data in orders_data:
        order = Orders(**data)
        db.session.add(order)
    db.session.commit()


def add_orders_elements():
    order_elements = []

    # delete old elements
    db.session.query(OrdersElements).delete()
    db.session.execute(text("ALTER SEQUENCE orders_elements_id_seq RESTART WITH 1"))

    # add new orders
    orders = Orders.query.all()
    bar = ChargingBar(
        f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]   Filling orders",
        max=len(Orders.query.all()),
        suffix="%(index)d/%(max)d",
    )
    for order in orders:
        bar.next()
        order_price = 0
        categories = Categories.query.all()
        used_goods = []
        elements_limit = 10

        # add goods of random categories
        for category in random.sample(categories, random.randint(1, len(categories))):
            # only bought goods (i.e. expense elements) are used in order
            bought_goods_data = (
                ExpensesElements.query.join(ExpensesElements.product)
                .filter(Goods.category == category)
                .all()
            )

            if len(used_goods) >= elements_limit:
                break
            if not bought_goods_data:
                continue

            # add from 3 to 5 elements
            for _ in range(3, 5):
                available_goods_data = [
                    product
                    for product in bought_goods_data
                    if product not in used_goods
                ]
                if available_goods_data:
                    product_data = random.choice(available_goods_data)
                    used_goods.append(product_data)
                    instock_quantity = sum(
                        elem.quantity
                        for elem in bought_goods_data
                        if elem.product == product_data.product
                    ) - sum(
                        elem["quantity"]
                        for elem in order_elements
                        if elem["product"] == product_data.product
                    )
                    if instock_quantity == 0:
                        continue

                    quantity = random.randint(1, min(int(instock_quantity), 10))
                    element_price = random.randint(10, 25) * 2.20
                    order_price += quantity * element_price

                    order_elements.append(
                        {
                            "order": order,
                            "product": product_data.product,
                            "quantity": quantity,
                            "price": element_price,
                        }
                    )
                else:
                    break
        # delete order if no elements were added
        if len(used_goods) == 0:
            db.session.delete(order)
            db.session.commit()
        else:
            order.price = round(order_price)
            db.session.add(order)

    # commit new orders
    for data in order_elements:
        order_element = OrdersElements(**data)
        db.session.add(order_element)
    db.session.commit()

    bar.finish()


def populate_fake_data(selected_lang=lang):
    global lang
    lang = selected_lang
    with app.app_context():
        time_started = datetime.now()
        print(
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Generating data from {starting_date.strftime('%Y-%m-%d')} with language set to {lang}"
        )
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]  Dropping db")
        db.drop_all()
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]  Creating db")
        db.create_all()

        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]  Resetting settings")
        util_reset_settings(lang=lang)
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]  Adding categories")
        add_categories()
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]  Adding user")
        add_user()
        print(
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]  Adding registration code"
        )
        add_reg_code()
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]  Adding goods")
        add_goods()
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]  Adding suppliers")
        add_suppliers()
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]  Adding customers")
        add_customers()
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]  Adding expenses")
        add_expenses()
        add_expenses_elms()
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]  Adding orders")
        add_orders()
        add_orders_elements()
        print(
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Done in {datetime.now() - time_started}"
        )


if __name__ == "__main__":
    populate_fake_data()
