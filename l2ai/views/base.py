from datetime import datetime
import logging
from flask import Blueprint, jsonify, make_response, request
from l2ai.extensions import cognito

blueprint = Blueprint("base", __name__)
logger = logging.getLogger(__name__)


@blueprint.route("/login", methods=["POST"])
def login():
    auth = request.authorization

    if auth is None or not (auth.username and auth.password):
        return make_response({'Message': 'Login credentials are required'}, 401)

    res = cognito.login(auth.username, auth.password)
    # res = {"abc": "123"}
    return jsonify(res)
