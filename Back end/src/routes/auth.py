from .. import db
from flask import jsonify, request, Blueprint
from flask_jwt_extended import create_access_token
from src.models.auth import User, RegistrationCode
from src.utils.auth import util_create_new_user

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["POST"])
def login():
    user_data = request.get_json()
    required_data = {"username", "password"}
    if not len(required_data - set(user_data.keys())):
        user_obj = User.query.filter_by(username=user_data["username"]).first()
        if not user_obj:
            return "Authorisation failed", 401

        if user_obj.check_password(user_data["password"]):
            jwt_token = create_access_token(identity=user_obj.username)

            return {"token": jwt_token}, 200
        else:
            return "Authorisation failed", 401
    return "Missing required data.", 406


@auth.route("/register", methods=["POST"])
def register():
    user_data = request.get_json()
    required_data = {"username", "password", "code"}
    if not len(required_data - set(user_data.keys())):
        code_obj = RegistrationCode.query.filter_by(code=user_data["code"]).first()

        # check the code
        if not code_obj:
            return "Invalid registration code.", 400

        new_user_data = util_create_new_user(
            username=user_data["username"], password=user_data["password"]
        )
        if new_user_data["code"] == 1:
            return "Username must be unique.", 400

        jwt_token = create_access_token(identity=new_user_data["user"].username)

        # invalidate the code
        db.session.delete(code_obj)
        db.session.commit()

        return {"token": jwt_token}, 200
    return "Missing required data.", 406
