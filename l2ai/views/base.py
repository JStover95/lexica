from base64 import b64decode
import logging
from flask import Blueprint, jsonify, make_response, request
from l2ai.collections import users
from l2ai.extensions import cognito, mongo

blueprint = Blueprint("base", __name__)
logger = logging.getLogger(__name__)


@blueprint.route("/login", methods=["POST"])
def login():
    auth = request.headers.get("Authorization")

    if auth is None:
        return make_response(
            {"Message": "Login credentials are required."},
            401
        )
    else:
        auth_decoded = b64decode(auth.split(" ")[1]).decode()

    try:
        email, password = auth_decoded.split(":")
    except ValueError:
        raise ValueError("Error retreiving login credentials.")

    user = users.find_one({"email": email})
    if user is None:
        return make_response({"Message": "Invalid email."}, 403)
    else:
        username = user["username"]

    res = cognito.login(username, password)
    return jsonify(res)
