from base64 import b64decode
import logging
from flask import Blueprint, jsonify, make_response, request
from l2ai.collections import users
from l2ai.extensions import cognito

blueprint = Blueprint("base", __name__)
logger = logging.getLogger(__name__)


@blueprint.route("/login", methods=["POST"])
def login():
    res_missing = {"Message": "Login credentials are required."}, 401
    res_retrieve = {"Message": "Error retrieving login credentials."}, 401
    res_invalid = {"Message": "Invalid login credentials."}, 403
    auth = request.headers.get("Authorization")

    if auth is None:
        return make_response(*res_missing)
    else:
        auth_decoded = b64decode(auth.split(" ")[1]).decode()

    try:
        username, password = auth_decoded.split(":")
    except ValueError:
        return make_response(*res_retrieve)

    user = users.find_one({"username": username})
    if user is None:
        return make_response(*res_invalid)

    res = cognito.login(username, password)
    if res is False:
        return make_response(*res_invalid)

    return jsonify(res)
