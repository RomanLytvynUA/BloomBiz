import argparse
from sqlalchemy import inspect
from src import db, app
from src.models.goods import *
from src.models.suppliers import *
from src.models.expenses import *
from src.models.settings import *
from src.models.customers import *
from src.models.auth import *

from src.utils.settings import util_reset_settings


# Create the database tables (for cli)
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Set up the database.")
    parser.add_argument(
        "--lang",
        type=str,
        choices=["ukr", "eng"],
        default="eng",
        help="language of inital data (ukr/eng)",
    )

    with app.app_context():
        db.drop_all()
        db.create_all()
        util_reset_settings(parser.parse_args().lang)


# check if a table is missing before creating
def soft_db_setup():
    with app.app_context():
        defined_tables = set(db.metadata.tables.keys())
        for table in defined_tables:
            if not inspect(db.engine).has_table(table):
                db.drop_all()
                db.create_all()
                util_reset_settings()
                break
