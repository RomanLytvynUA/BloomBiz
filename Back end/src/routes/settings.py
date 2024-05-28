from .. import db
from flask import jsonify, request, Blueprint
from ..utils.settings import util_set_settings, util_reset_settings, util_generate_settings_dict

settings = Blueprint("settings", __name__)


@settings.route('/get', methods=['GET'])
def get_settings():
    return jsonify(util_generate_settings_dict())


@settings.route('/edit', methods=['PUT'])
def edit_settings():
    data = request.get_json()

    for name, value in data.items():
        util_set_settings(name, value)

    return "Edited settings successfully.", 200


@settings.route('/reset', methods=['POST'])
def reset_settings():
    util_reset_settings()

    return "Reset settings successfully.", 200
