from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object("src.config")
db = SQLAlchemy(app)
jwt = JWTManager(app)
CORS(
    app,
    resources={
        r"/*": {"origins": ["http://localhost:5173/*", "http://localhost:500/*"]}
    },
)

from .routes.goods import goods
from .routes.expenses import expenses
from .routes.suppliers import suppliers
from .routes.orders import orders
from .routes.settings import settings
from .routes.customers import customers
from .routes.auth import auth

# from .routes.swagger import swaggerui_blueprint

app.register_blueprint(goods, url_prefix="/goods")
app.register_blueprint(expenses, url_prefix="/expenses")
app.register_blueprint(suppliers, url_prefix="/suppliers")
app.register_blueprint(orders, url_prefix="/orders")
app.register_blueprint(settings, url_prefix="/settings")
app.register_blueprint(customers, url_prefix="/customers")
app.register_blueprint(auth, url_prefix="/auth")
# app.register_blueprint(swaggerui_blueprint)
