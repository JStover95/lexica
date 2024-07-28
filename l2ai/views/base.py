from base64 import b64decode
from flask import Blueprint, make_response, request
from l2ai.extensions import cognito
from l2ai.json_schemas import Base, validate_schema
from l2ai.models import User
from l2ai.schema import UserInput
from l2ai.utils.cognito import get_access_token_from_request
from l2ai.utils.handlers import handle_server_error
from l2ai.utils.logging import logger

blueprint = Blueprint("base", __name__)


@blueprint.route("/login")
def login():
    """
    Login a user using the username and password in the Authorization header.
    Upon successful login, an Access Token and Refresh Token are sent to the
    client in "access_token" and "refresh_token" cookies.

    Methods:
        GET

    Required Headers:
        Authorization

    Responses:
        code: 200
        body:
         - Message (str): "Challenge requested by server."
         - ChallengeName (str): A challenge name as returned by the AWS
           InitiateAdminAuth endpoint.
         - Session (str): The session key as returned by the AWS InitiateAdminAuth
           endpoint.
         - ChallengeParameters (object): The challenge parameters as returned by the AWS
           InitiateAdminAuth endpoint.
        Generated when the Cognito Identity Client responds to a login request
        with an authorization challenge.

        code: 200
        body:
         - Message (str): "Successful login."
        Generated upon successful login.

        code: 401
        body:
         - Message (str): "Login credentials are required."
        Generated when a request is made without an Authorization header.

        code: 401
        body:
         - Message (str): "Error retrieving login credentials"
        Generated when the Authorization header is formatted incorrectly.

        code: 403
        body:
         - Message (str): "Invalid login credentials"
        Generated when the client provides incorrect credentials.

        code: 500
        body:
         - Message (str): "Failure verifying access token."
        Generated when the Access Token returned from the Cognito Identity
        Provider could not be verified after successful login.
    """
    auth = request.headers.get("Authorization")

    if auth is None:
        return make_response({"Message": "Login credentials are required."}, 401)
    else:
        auth_decoded = b64decode(auth.split(" ")[1]).decode()

    try:
        username, password = auth_decoded.split(":")
    except ValueError:
        return make_response({"Message": "Error retrieving login credentials."}, 401)

    user: UserInput | None = User.objects.find_one({"username": username})
    if user is None:
        return make_response({"Message": "Invalid login credentials."}, 403)

    auth_result = cognito.login(username, password)
    if auth_result is False:
        return make_response({"Message": "Invalid login credentials."}, 403)

    if "ChallengeName" in auth_result:
        res = {
            "Message": "Challenge requested by server.",
            "ChallengeName": auth_result["ChallengeName"],
            "Session": auth_result["Session"],
            "ChallengeParameters": auth_result["ChallengeParameters"]
        }

        return make_response(res, 200)

    try:
        access_token = auth_result["AuthenticationResult"]["AccessToken"]
        refresh_token = auth_result["AuthenticationResult"]["RefreshToken"]
    except KeyError:
        return handle_server_error("Failure retrieving access and refresh tokens.", 500, e)

    try:
        cognito.get_claim_from_access_token(access_token)
    except Exception as e:
        return handle_server_error("Failure verifying access token.", 500, e)

    response = make_response(
        {
            "ID": user._id,
            "Username": user.username,
            "AccessToken": access_token,
            "RefreshToken": refresh_token
        },
        200
    )

    return response


@blueprint.route("/verify")
def verify():
    logger.info("Tests for base.verify not implemented.")

    try:
        access_token = get_access_token_from_request()
        claim = cognito.get_claim_from_access_token(access_token)

    except Exception as e:
        logger.exception(e)
        res = {"IsAuthenticated": False}
        return make_response(res, 403)

    res = {"IsAuthenticated": True, "Username": claim["username"]}
    return make_response(res, 200)


@blueprint.route("/challenge", methods=["POST"])
@validate_schema(Base.challenge_schema)
def challenge(validated_data: Base.ChallengeRequestType):
    """
    Respond to an authorization challenge if one was requested by the Cognito
    Identity Provider. Upon successful login, an Access Token and Refresh Token
    are sent to the client in "access_token" and "refresh_token" cookies.

    Methods:
        POST

    Request Body:
        Username (str): The user responding to the challenge.
        ChallengeName (str): The name of the challenge as required by the
            Cognito RespondToAuthChallenge endpoint.
        Session (str): The session key as required by the Cognito
            RespondToAuthChallenge endpoint.
        ChallengeResponses (object): The challenge response parameters as
            required by the Cognito RespondToAuthChallenge endpoint.

    Responses:
        code: 200
        body:
         - Message (str): "Login successful."
        Generated upon successful login.

        code: 401
        body:
         - Message (str): "Missing paylod."
        Generated when no payload is sent with the request.

        code: 401
        body:
         - Message (str): "Incorrect payload."
        Generated when an incorrect payload is sent with the request.

        code: 403
        body:
         - Message (str): "Invalid challenge response."
        Generated when the challenge response fails.

        code: 500
        body:
         - Message (str): "Failure verifying access token."
        Generated when the Access Token returned from the Cognito Identity
        Provider could not be verified after successful login. 
    """
    username = validated_data["Username"]

    kwargs = {
        "ChallengeName": validated_data["ChallengeName"],
        "ChallengeResponses": validated_data["ChallengeResponses"],
        "Session": validated_data["Session"],
    }

    auth_result = cognito.respond_to_challenge(username, kwargs)

    if auth_result is False:
        return make_response({"Message": "Invalid challenge response."}, 403)

    try:
        access_token = auth_result["AuthenticationResult"]["AccessToken"]
        refresh_token = auth_result["AuthenticationResult"]["RefreshToken"]
    except Exception as e:
        return handle_server_error("Failure retrieving access and refresh tokens.", 500, e)

    try:
        cognito.get_claim_from_access_token(access_token)
    except Exception as e:
        return handle_server_error("Failure verifying access token.", 500, e)

    response = make_response(
        {
            "Message": "Login successful.",
            "AccessToken": access_token,
            "RefreshToken": refresh_token
        },
        200
    )
    # set_access_cookies(response, auth_result)

    return response


@blueprint.route("/logout", methods=["POST"])
@cognito.login_required
@validate_schema(Base.logout_schema)
def logout(validated_data: Base.LogoutRequestType):
    """
    Logout a user. This will invalidate the user's Access Token with the Cognito
    Identity Provider and attempt to delete the access_token and refresh_token
    cookies from the client's browser.

    Methods:
        POST

    Request body:
        Username (str): the user to log out.

    Responses:
        code: 200
        body:
         - Message (str): "Logged out successfully."
        Generated upon successful logout.

        code: 401
        body:
         - Message (str): "Missing paylod."
        Generated when no payload is sent with the request.

        code: 401
        body:
         - Message (str): "Incorrect payload."
        Generated when an incorrect payload is sent with the request.
    """
    username = validated_data["Username"]
    cognito.sign_out(username)
    response = make_response({"Message": "Logged out successfully"}, 200)
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")

    return response


@blueprint.route("/forgot-password", methods=["POST"])
@validate_schema(Base.forgot_password_schema)
def forgot_password(validated_data: Base.ForgotPasswordRequestType):
    """
    Create a request to reset a user's password. This will send a confirmation
    code to the user's default verification method.

    Methods:
        POST

    Request body:
        Username (str): the user to request the password reset for

    Responses:
        code: 200
        body:
         - Message (str): "Confirmation code sent successfully."
         - CodeDeliveryDetails (object): details of how the verification code
           was sent, according to the Cognito ForgotPassword API endpoint.
        Generated upon successfully sending the verification code.

        code: 401
        body:
         - Message (str): "Missing paylod."
        Generated when no payload is sent with the request.

        code: 401
        body:
         - Message (str): "Incorrect payload."
        Generated when an incorrect payload is sent with the request.
    """
    username = validated_data["Username"]
    auth_result = cognito.forgot_password(username)

    res = {
        "Message": "Confirmation code sent successfully.",
        "CodeDeliveryDetails": auth_result["CodeDeliveryDetails"]
    }

    response = make_response(res, 200)

    return response


@blueprint.route("/confirm-forgot-password", methods=["POST"])
@validate_schema(Base.confirm_forgot_password_schema)
def confirm_forgot_password(
        validated_data: Base.ConfirmForgotPasswordRequestType
    ):
    """
    Reset a user's password using the Confirmation Code returned by the
    forgot_password endpoint.

    Methods:
        POST

    Request body:
        Username (str): the user to reset the password of
        ConfirmationCode (str): the Confirmation Code as returned by the
            forgot_password endpoint
        Password (str): the user's new password

    Responses:
        code: 200
        body:
         - Message (str): "Password successfully reset."
        Generated upon successfully resetting the user's password.

        code: 401
        body:
         - Message (str): "Missing paylod."
        Generated when no payload is sent with the request.

        code: 401
        body:
         - Message (str): "Incorrect payload."
        Generated when an incorrect payload is sent with the request.
    """
    cognito.confirm_forgot_password(
        validated_data["Username"],
        validated_data["ConfirmationCode"],
        validated_data["Password"]
    )

    res = make_response({"Message": "Password successfully reset."}, 200)

    return res


@blueprint.route("/refresh", methods=["POST"])
@validate_schema(Base.refresh_schema)
def refresh(validated_data: Base.RefreshRequestType):
    """
    Refresh a user's Access Token using the refrest_token cookie. Upon
    successful verification of the user's Refresh Token, this endpoint sets a
    new access_token and refresh_token cookies.

    Methods:
        GET

    Responses:
        code: 200
        body:
         - Message (str): "Access token successfully refreshed."
        Generated upon successful refresh.

        code: 401
        body:
         - Message (str): "access_token or refresh_token cookies are not
           present."
        Generated if the required cookies are not present in the request.

        code: 500
        body:
         - Message (str): "Error refreshing access token."
        Generated either when the claim from the access token could not be
        verified or when the Access Token could not be refreshed.
    """
    # try:
    #     access_token = request.cookies["access_token"]
    #     refresh_token = request.cookies["refresh_token"]

    # except BadRequestKeyError as e:
    #     return make_response({"Message": "access_token or refresh_token cookies are not present."}, 401)

    access_token = validated_data["AccessToken"]

    try:
        claim = cognito.get_claim_from_access_token(access_token)
    except Exception as e:
        return handle_server_error("Error refreshing access token.", 500, e)

    refresh_token = validated_data["RefreshToken"]

    try:
        auth_result = cognito.refresh(claim["username"], refresh_token)
    except Exception as e:
        return handle_server_error("Error refreshing access token.", 403, e)

    try:  # TODO: create function with duplicate code
        access_token = auth_result["AuthenticationResult"]["AccessToken"]
    except Exception as e:
        return handle_server_error("Failure retrieving access token.", 500, e)

    try:
        cognito.get_claim_from_access_token(access_token)
    except Exception as e:
        return handle_server_error("Failure verifying access token.", 500, e)

    response = make_response(
        {
            "Message": "Access token successfully refreshed.",
            "AccessToken": access_token
        },
        200
    )
    # set_access_cookies(response, auth_result)

    return response
