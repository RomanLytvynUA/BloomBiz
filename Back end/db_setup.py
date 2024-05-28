from src import db, app
from src.models.goods import *
from src.models.suppliers import *
from src.models.expenses import *
from src.models.settings import *

# Create the database tables
with app.app_context():
    db.drop_all()
    db.create_all()
