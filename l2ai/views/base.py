from base64 import b64decode
from flask import Blueprint, make_response, request
from l2ai.collections import users
from l2ai.extensions import cognito
from l2ai.schemas import Base, validate_schema
from l2ai.utils.cognito import set_access_cookies
from l2ai.utils.logging import logger

blueprint = Blueprint("base", __name__)


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

    if "ChallengeName" in auth_result:
        return make_response(
            {
                "ChallengeName": auth_result["ChallengeName"],
                "Session": auth_result["Session"],
                "ChallengeParameters": auth_result["ChallengeParameters"]
            },
            200
        )

    try:
        access_token = auth_result["AuthenticationResult"]["AccessToken"]
        cognito.verify_claim(access_token)

    except Exception as e:
        logger.exception(e)
        return make_response(*res_token)

    response = make_response(*res_successful)
    set_access_cookies(response, auth_result)
    return response


@blueprint.route("/challenge", methods=["POST"])
@validate_schema(Base.challenge_schema)
def challenge(validated_data: Base.ChallengeRequestType):
    res_invalid = {"Message": "Invalid challenge response."}, 403
    res_token = {"Message": "Failure verifying access token."}, 401
    res_successful = {"Message": "Login successful"}, 200

    username = validated_data["Username"]
    kwargs = {
        "ChallengeName": validated_data["ChallengeName"],
        "ChallengeResponses": validated_data["ChallengeResponses"],
        "Session": validated_data["Session"],
    }

    auth_result = cognito.respond_to_challenge(username, kwargs)

    if auth_result is False:
        return make_response(*res_invalid)

    try:
        access_token = auth_result["AuthenticationResult"]["AccessToken"]
        cognito.verify_claim(access_token)

    except Exception as e:
        logger.exception(e)
        return make_response(*res_token)

    response = make_response(*res_successful)
    set_access_cookies(response, auth_result)
    return response


@blueprint.route("/logout", methods=["POST"])
@cognito.login_required
@validate_schema(Base.logout_schema)
def logout(validated_data: Base.LogoutRequestType):
    res_success = {"Message": "Logged out successfully"}, 200
    username = validated_data["Username"]
    cognito.sign_out(username)
    response = make_response(*res_success)
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")

    return response


@blueprint.route("/forgot-password", methods=["POST"])
@validate_schema(Base.forgot_password_schema)
def forgot_password(validated_data: Base.ForgotPasswordRequestType):
    username = validated_data["Username"]
    auth_result = cognito.forgot_password(username)

    res = {
        "Message": "Confirmation code sent successfully.",
        "CodeDeliveryDetails": auth_result["CodeDeliveryDetails"]
    }

    response = make_response(res, 200)

    return response


@blueprint.route("/confirm-forgot-password", methods=["POST"])
def confirm_forgot_password():
    return make_response("success", 200)


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
    set_access_cookies(response, auth_result)
    return response


@blueprint.route("/protected")
@cognito.login_required
def protected():
    return make_response("success", 200)
