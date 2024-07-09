from src import db
from src.models.auth import User


def util_create_new_user(username, password):
    if User.query.filter_by(username=username).first():
        return {"user": None, "code": 1, "message": "Duplicated username"}
    else:
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return {"user": new_user, "code": 0, "message": "Created user successfuly"}
