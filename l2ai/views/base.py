from base64 import b64decode
from functools import wraps
import logging
import time
from flask import Blueprint, make_response, request
from werkzeug.exceptions import BadRequestKeyError
from l2ai.collections import users
from l2ai.extensions import cognito

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

    res = cognito.login(username, password)
    if res is False:
        return make_response(*res_invalid)

    try:
        access_token = res["AuthenticationResult"]["AccessToken"]
        refresh_token = res["AuthenticationResult"]["RefreshToken"]
        claim = cognito.verify_claim(access_token)

    except Exception as e:
        logger.exception(e)
        return make_response(*res_token)

    response = make_response(*res_successful)

    response.set_cookie(
        "X-AccessToken",
        access_token,
        expires=claim["exp"],
        secure=True,
        httponly=True,
        samesite="Strict"
    )

    response.set_cookie(
        "X-RefreshToken",
        refresh_token,
        expires=claim["exp"],
        secure=True,
        httponly=True,
        samesite="Strict"
    )

    return response


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        res_unauthorized = {"Message": "Unauthorized request."}, 403
        res_refresh = {"Message": "Error occured while refreshing token."}, 500

        try:
            access_token = request.cookies["X-AccessToken"]

        except BadRequestKeyError:
            logger.warn("Request made without X-AccessToken header.")
            return make_response(*res_unauthorized)

        try:
            refresh_token = request.cookies["X-RefreshToken"]

        except KeyError:
            logger.warn("RefreshToken header missing from request.")
            return make_response(*res_unauthorized)

        try:
            claim = cognito.verify_claim(access_token)

        except Exception as e:
            logger.exception(e)
            return make_response(*res_unauthorized)

        if time.time() > claim["exp"]:
            return make_response(*res_unauthorized)

        try:
            if time.time() - 300 > claim["auth_time"]:
                res = cognito.refresh(claim["username"], refresh_token)
                access_token = res["AuthenticationResult"]["AccessToken"]
                refresh_token = res["AuthenticationResult"]["RefreshToken"]
                claim = cognito.verify_claim(access_token)
                # how to add to response?

        except Exception as e:
            logger.exception(e)
            return make_response(*res_refresh)

        return f(*args, **kwargs)

    return wrapper


@blueprint.route("/protected")
@login_required
def protected():
    return make_response("success", 200)
