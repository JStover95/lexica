from base64 import b64decode
from functools import wraps
import logging
import time
from flask import Blueprint, make_response, request
from mypy_boto3_cognito_idp.type_defs import InitiateAuthResponseTypeDef
from werkzeug import Response
from l2ai.collections import users
from l2ai.extensions import cognito
from l2ai.utils.cognito import set_access_cookies

blueprint = Blueprint("base", __name__)
logger = logging.getLogger(__name__)


@blueprint.route("/login", methods=["POST"])
def login():
    res_missing = {"Message": "Login credentials are required."}, 401
    res_retrieve = {"Message": "Error retrieving login credentials."}, 401
    res_invalid = {"Message": "Invalid login credentials."}, 403
    res_token = {"Message": "Failure verifying access token."}, 401
    res_successful = {"Message": "Login successful"}, 200

    auth = request.headers.get("Authorization")

    if auth is None:
        return make_response(*res_missing)
    else:
        auth_decoded = b64decode(auth.split(" ")[1]).decode()

    try:
        username, password = auth_decoded.split(":")
    except ValueError as e:
        logger.exception(e)
        return make_response(*res_retrieve)

    user = users.find_one({"username": username})
    if user is None:
        return make_response(*res_invalid)

    auth_result = cognito.login(username, password)
    if auth_result is False:
        return make_response(*res_invalid)

    try:
        access_token = auth_result["AuthenticationResult"]["AccessToken"]
        claim = cognito.verify_claim(access_token)

    except Exception as e:
        logger.exception(e)
        return make_response(*res_token)

    response = make_response(*res_successful)
    set_access_cookies(response, auth_result, claim)
    return response


@blueprint.route("/refresh")
def refresh():
    res_unauthorized = {"Message": "Unauthorized request."}, 403
    res_exception = {"Message": "Error refreshing access token."}, 500
    res_success = {"Message": "Access token successfully refreshed"}, 200

    access_token = request.cookies["access_token"]
    refresh_token = request.cookies["refresh_token"]

    try:
        claim = cognito.verify_claim(access_token)

    except Exception as e:
        logger.exception(e)
        return make_response(*res_unauthorized)

    try:
        auth_result = cognito.refresh(claim["username"], refresh_token)

    except Exception as e:
        logger.exception(e)
        return make_response(*res_exception)

    response = make_response(*res_success)
    set_access_cookies(response, auth_result, claim)
    return response


@blueprint.route("/protected")
@cognito.login_required
def protected():
    return make_response("success", 200)
