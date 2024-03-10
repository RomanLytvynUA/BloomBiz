import os

user = os.getenv("FLASK_USER")
password = os.getenv("FLASK_PASSWORD")
SQLALCHEMY_DATABASE_URI = f'postgresql://{user}:{password}@localhost/BloomBiz DB'
DEBUG = True
