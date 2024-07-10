from src import db
from src.models.auth import User
from src.utils.auth import util_create_new_user
from testing_data import clear_db


def test_user_password(app_client):
    """
    GIVEN -
    WHEN creating a user
    THEN password is hashed;
         password can be validated.
    """
    clear_db()

    new_user = User(username="user", password="password123")
    db.session.add(new_user)
    db.session.commit()

    assert new_user.password != "password123"
    assert new_user.check_password("password123")


def test_util_create_new_user(app_client):
    """
    GIVEN -
    WHEN calling create user util with valid details
    THEN user is created;
         output contains valid user object.
    """
    clear_db()

    output = util_create_new_user("name", "password")
    queried_user = User.query.filter_by(username="name").first()

    assert queried_user
    assert output["user"] == queried_user


def test_util_create_new_user_duplicate(app_client):
    """
    GIVEN db containing a user instance
    WHEN calling create user util with a duplicated username
    THEN new user is not created;
         output contains None as user object.
    """
    clear_db()

    new_user = User(username="name", password="password123")
    db.session.add(new_user)
    db.session.commit()

    output = util_create_new_user("name", "password")
    queried_user = User.query.filter_by(username="name").all()

    assert len(queried_user) == 1
    assert output["user"] == None
