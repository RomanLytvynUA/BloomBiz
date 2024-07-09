from src import db, app
from src.models.goods import *
from src.models.suppliers import *
from src.models.expenses import *
from src.models.settings import *
from src.models.customers import *
from src.models.auth import *

from src.utils.settings import util_reset_settings


# Create the database tables
with app.app_context():
    db.drop_all()
    db.create_all()
    util_reset_settings()
