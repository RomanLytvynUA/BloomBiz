import os
from datetime import timedelta

SQLALCHEMY_DATABASE_URI = os.getenv("BB_DB_URI")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=10)
DEBUG = True
