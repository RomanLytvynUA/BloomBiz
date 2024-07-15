import json
from flask_jwt_extended import decode_token
import requests
from src import db
from src.models.auth import User, RegistrationCode
from tests.testing_data import clear_db


def test_jwt_required(urls, app_client):
    """
    GIVEN all app routes
    WHEN sending a request to a route with no/invalid jwt
    THEN response contains a 401 or a 422 error.
    """

    for name, route in urls.items():
        if "auth" in route["route"]:
            # skip auth routes
            continue

        if "del" in name:
            # deletion requires an id passed in the url
            route["route"] += "/0"

        no_token_response = requests.request(url=route["route"], method=route["method"])
        invalid_token_response = requests.request(
            url=route["route"],
            method=route["method"],
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer FAKE_JWT",
            },
        )

        assert no_token_response.status_code == 401
        assert invalid_token_response.status_code == 422


def test_login(urls, app_client):
    """
    GIVEN db containing a user credentials
    WHEN logging in with the credentials
    THEN proper jwt is returned.
    PROVIDED required data is present.
    """
    clear_db()
    route = urls["login"]

    new_user = User(username="name", password="password")
    db.session.add(new_user)
    db.session.commit()

    positive_response = requests.request(
        url=route["route"],
        method=route["method"],
        json={"username": new_user.username, "password": "password"},
        headers={"Content-Type": "application/json"},
    )

    negative_response = requests.request(
        url=route["route"],
        method=route["method"],
        json={},
        headers={"Content-Type": "application/json"},
    )

    assert positive_response.status_code == 200
    assert decode_token(json.loads(positive_response.text)["token"])
    assert negative_response.status_code == 406


def test_login_invalid_credantials(urls, app_client):
    """
    GIVEN
    WHEN logging in with invalid credentials
    THEN 401 error is returned.
    """
    clear_db()
    route = urls["login"]

    response = requests.request(
        url=route["route"],
        method=route["method"],
        json={"username": "fake_name", "password": "fake_password"},
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 401


def test_registration(urls, app_client):
    """
    GIVEN a valid registration code
    WHEN sending a registration request with valid data
    THEN user is created, the code is invalidated.
    """
    clear_db()
    route = urls["register"]

    code = RegistrationCode(code="reg_code")
    db.session.add(code)
    db.session.commit()

    response = requests.request(
        url=route["route"],
        method=route["method"],
        json={"username": "name", "password": "password", "code": "reg_code"},
        headers={"Content-Type": "application/json"},
    )

    queried_user = User.query.filter_by(username="name").first()
    queried_code = RegistrationCode.query.filter_by(code="reg_code").first()

    assert queried_user
    assert not queried_code
    assert response.status_code == 200


def test_registration_invalid_code(urls, app_client):
    """
    GIVEN
    WHEN sending a registration request with an invalid registration code
    THEN user is NOT created, error response is returned.
    """
    clear_db()
    route = urls["register"]

    response = requests.request(
        url=route["route"],
        method=route["method"],
        json={"username": "name", "password": "password", "code": "fake_code"},
        headers={"Content-Type": "application/json"},
    )

    queried_user = User.query.filter_by(username="name").first()

    assert not queried_user
    assert response.status_code == 400


def test_registration_duplicated_username(urls, app_client):
    """
    GIVEN a valid registration code and a user
    WHEN sending a registration request with an existing username
    THEN user is NOT created, error response is returned.
    """
    clear_db()
    route = urls["register"]

    new_user = User(username="name", password="password")
    db.session.add(new_user)
    code = RegistrationCode(code="reg_code")
    db.session.add(code)
    db.session.commit()

    response = requests.request(
        url=route["route"],
        method=route["method"],
        json={"username": new_user.username, "password": "password", "code": "code"},
        headers={"Content-Type": "application/json"},
    )

    queried_user = User.query.filter_by(username="name").all()

    assert len(queried_user) == 1
    assert response.status_code == 400
