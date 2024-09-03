from base64 import b64decode
from flask import Blueprint, make_response, request
from app.extensions import cognito
from app.collections import User, users
from app.json_schemas import Base, validate_schema
from app.utils.cognito import get_access_token_from_request
from app.utils.handlers import handle_server_error
from app.utils.logging import logger

blueprint = Blueprint("base", __name__)


@blueprint.route("/login")
def login():
    """
    Authenticate a user using credentials from the Authorization header.

    This endpoint allows a user to log in by providing a username and password
    in the Authorization header. Upon successful login, an Access Token and
    Refresh Token are returned to the client. The endpoint also handles
    authorization challenges from the AWS Cognito Identity Provider.

    Headers:
        Authorization (str): Basic authentication header containing the username
        and  password encoded in Base64
        (format: `Basic base64(username:password)`).

    Responses:
        200 OK:
            - If login requires additional authorization:
                {
                    "Message": "Challenge requested by server.",
                    "ChallengeName": <ChallengeName>,
                    "Session": <Session>,
                    "ChallengeParameters": <ChallengeParameters>
                }
            - If login is successful:
                {
                    "Message": "Successful login.",
                    "ID": <User ID>,
                    "Username": <Username>,
                    "AccessToken": <AccessToken>,
                    "RefreshToken": <RefreshToken>
                }
        
        401 Unauthorized:
            - If the Authorization header is missing:
                {
                    "Message": "Login credentials are required."
                }
            - If the Authorization header is incorrectly formatted:
                {
                    "Message": "Error retrieving login credentials."
                }
        
        403 Forbidden:
            - If the provided credentials are invalid:
                {
                    "Message": "Invalid login credentials."
                }
        
        500 Internal Server Error:
            - If there is a failure verifying the access token:
                {
                    "Message": "Failure verifying access token."
                }

    Example Responses:
        - Authorization challenge required:
            {
                "Message": "Challenge requested by server.",
                "ChallengeName": "SMS_MFA",
                "Session": "session_key",
                "ChallengeParameters": {...}
            }
        - Successful login:
            {
                "Message": "Successful login.",
                "ID": "123456",
                "Username": "user123",
                "AccessToken": "access_token_value",
                "RefreshToken": "refresh_token_value"
            }
        - Invalid credentials:
            {
                "Message": "Invalid login credentials."
            }
        - Missing credentials:
            {
                "Message": "Login credentials are required."
            }
        - Error retrieving credentials:
            {
                "Message": "Error retrieving login credentials."
            }
    """
    auth = request.headers.get("Authorization")

    # If the request is missing an Authorization header
    if auth is None:
        return make_response({"Message": "Login credentials are required."}, 401)
    else:
        auth_decoded = b64decode(auth.split(" ")[1]).decode()

    # If the Authorization header is not formatted properly
    try:
        username, password = auth_decoded.split(":")
    except ValueError:
        return make_response({"Message": "Error retrieving login credentials."}, 401)

    # If the user provided an invalid username
    user: User | None = users.find_one({"username": username})
    if user is None:
        return make_response({"Message": "Invalid login credentials."}, 403)

    # If the user provided an invalid password
    auth_result = cognito.login(username, password)
    if auth_result is False:
        return make_response({"Message": "Invalid login credentials."}, 403)

    # If Cognito responded with an authorization challenge
    if "ChallengeName" in auth_result:
        res = {
            "Message": "Challenge requested by server.",
            "ChallengeName": auth_result["ChallengeName"],
            "Session": auth_result["Session"],
            "ChallengeParameters": auth_result["ChallengeParameters"]
        }

        return make_response(res, 200)

    # Retrieve the access and refresh tokens from the Cognito response
    try:
        access_token = auth_result["AuthenticationResult"]["AccessToken"]
        refresh_token = auth_result["AuthenticationResult"]["RefreshToken"]
    except KeyError:
        return handle_server_error("Failure retrieving access and refresh tokens.", 500, e)

    # Verify that the access token is valid
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
    """
    Verify the validity of a user's JWT provided in the Authorization header.

    This endpoint checks whether the JWT provided in the request's Authorization
    header is valid. If the token is valid, the endpoint returns a JSON response
    indicating that the user is authenticated, along with their username.
    If the token is invalid or an error occurs during verification, the endpoint
    returns a 403 Forbidden response.

    Returns:
        Response: A JSON response containing:
            - IsAuthenticated (bool): True if the JWT is valid, False otherwise.
            - Username (str, optional): The username extracted from the valid
                JWT. This field is only present if the JWT is valid.
        HTTP Status:
            - 200 OK: If the JWT is valid and the user is authenticated.
            - 403 Forbidden: If the JWT is invalid or an error occurs during the
                verification process.

    Example Response:
        If the JWT is valid:
        {
            "IsAuthenticated": True,
            "Username": "user123"
        }

        If the JWT is invalid or an error occurs:
        {
            "IsAuthenticated": False
        }
    """
    try:
        # Extract the access token from the request's Authorization header
        access_token = get_access_token_from_request()

        # Verify the token and retrieve the claims (e.g., username) from the access token
        claim = cognito.get_claim_from_access_token(access_token)

    except Exception as e:
        logger.exception(e)

        # Return a response indicating that the user is not authenticated
        res = {"IsAuthenticated": False}
        return make_response(res, 403)

    # If the token is valid, return a response indicating the user is authenticated along with their username
    res = {"IsAuthenticated": True, "Username": claim["username"]}
    return make_response(res, 200)



@blueprint.route("/challenge", methods=["POST"])
@validate_schema(Base.challenge_schema)
def challenge(validated_data: Base.ChallengeRequestType):
    """
    Respond to a Cognito authorization challenge.

    This endpoint is used to respond to an authorization challenge issued by 
    the AWS Cognito Identity Provider. The client provides the necessary 
    challenge parameters, and upon successful response, access and refresh 
    tokens are returned.

    Request Body:
        - Username (str): The username of the user responding to the challenge.
        - ChallengeName (str): The type of challenge as specified by the Cognito 
            RespondToAuthChallenge endpoint.
        - Session (str): The session key returned by the Cognito InitiateAuth
            endpoint during the challenge request.
        - ChallengeResponses (dict): The response parameters required to 
            satisfy the challenge, such as verification codes or passwords.

    Responses:
        200 OK:
            - If the challenge is successfully responded to:
                {
                    "Message": "Login successful.",
                    "AccessToken": <AccessToken>,
                    "RefreshToken": <RefreshToken>
                }
        
        401 Unauthorized:
            - If the request is missing a payload:
                {
                    "Message": "Missing payload."
                }
            - If the payload is incorrectly formatted:
                {
                    "Message": "Incorrect payload."
                }

        403 Forbidden:
            - If the provided challenge response is invalid:
                {
                    "Message": "Invalid challenge response."
                }

        500 Internal Server Error:
            - If there is a failure verifying the access token after the
                challenge:
                {
                    "Message": "Failure verifying access token."
                }

    Example Responses:
        - Successful response:
            {
                "Message": "Login successful.",
                "AccessToken": "access_token_value",
                "RefreshToken": "refresh_token_value"
            }
        - Invalid challenge response:
            {
                "Message": "Invalid challenge response."
            }
        - Missing or incorrect payload:
            {
                "Message": "Missing payload."
            }
    """
    username = validated_data["Username"]

    # Prepare the necessary parameters for responding to the challenge
    kwargs = {
        "ChallengeName": validated_data["ChallengeName"],
        "ChallengeResponses": validated_data["ChallengeResponses"],
        "Session": validated_data["Session"],
    }

    # Attempt to respond to the challenge using the Cognito client
    auth_result = cognito.respond_to_challenge(username, kwargs)

    # If the challenge response is invalid, return a 403 Forbidden response
    if auth_result is False:
        return make_response({"Message": "Invalid challenge response."}, 403)

    # Try to retrieve access and refresh tokens from the Cognito response
    try:
        access_token = auth_result["AuthenticationResult"]["AccessToken"]
        refresh_token = auth_result["AuthenticationResult"]["RefreshToken"]
    except Exception as e:
        return handle_server_error("Failure retrieving access and refresh tokens.", 500, e)

    # Verify the access token by extracting claims
    try:
        cognito.get_claim_from_access_token(access_token)
    except Exception as e:
        return handle_server_error("Failure verifying access token.", 500, e)

    # Return a successful login response with access and refresh tokens
    response = make_response(
        {
            "Message": "Login successful.",
            "AccessToken": access_token,
            "RefreshToken": refresh_token
        },
        200
    )

    return response


# @blueprint.route("/logout", methods=["POST"])
# @cognito.login_required
# @validate_schema(Base.logout_schema)
# def logout(validated_data: Base.LogoutRequestType):
#     """
#     Logout a user. This will invalidate the user's Access Token with the Cognito
#     Identity Provider and attempt to delete the access_token and refresh_token
#     cookies from the client's browser.

#     Request body:
#         - Username (str): the user to log out.

#     Responses:
#         code: 200
#         body:
#          - Message (str): "Logged out successfully."
#         Generated upon successful logout.

#         code: 401
#         body:
#          - Message (str): "Missing paylod."
#         Generated when no payload is sent with the request.

#         code: 401
#         body:
#          - Message (str): "Incorrect payload."
#         Generated when an incorrect payload is sent with the request.
#     """
#     username = validated_data["Username"]
#     cognito.sign_out(username)
#     response = make_response({"Message": "Logged out successfully"}, 200)
#     response.delete_cookie("access_token")
#     response.delete_cookie("refresh_token")

#     return response


@blueprint.route("/forgot-password", methods=["POST"])
@validate_schema(Base.forgot_password_schema)
def forgot_password(validated_data: Base.ForgotPasswordRequestType):
    """
    Initiate the password reset process for a user.

    This endpoint triggers the AWS Cognito ForgotPassword API, which sends a 
    confirmation code to the user's default verification method (e.g., email or 
    phone) to begin the password reset process.

    Request Body:
        - Username (str): The username of the user requesting the password reset.

    Responses:
        200 OK:
            - If the confirmation code is sent successfully:
                {
                    "Message": "Confirmation code sent successfully.",
                    "CodeDeliveryDetails": <CodeDeliveryDetails>
                }

        401 Unauthorized:
            - If the request is missing a payload:
                {
                    "Message": "Missing payload."
                }
            - If the payload is incorrectly formatted:
                {
                    "Message": "Incorrect payload."
                }

    Example Response:
        - Successful confirmation code sent:
            {
                "Message": "Confirmation code sent successfully.",
                "CodeDeliveryDetails": {
                    "Destination": "example@example.com",
                    "DeliveryMedium": "EMAIL",
                    "AttributeName": "email"
                }
            }
    """
    username = validated_data["Username"]
    
    # Call Cognito's forgot password API to send a confirmation code
    auth_result = cognito.forgot_password(username)

    # Prepare the success response with the confirmation code delivery details
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
    Complete the password reset process using the confirmation code.

    This endpoint allows the user to reset their password by providing the 
    confirmation code received via the forgot_password endpoint and setting a 
    new password.

    Request Body:
        - Username (str): The username of the user resetting the password.
        - ConfirmationCode (str): The confirmation code received from the 
            forgot_password process.
        - Password (str): The new password to set for the user.

    Responses:
        200 OK:
            - If the password reset is successful:
                {
                    "Message": "Password successfully reset."
                }

        401 Unauthorized:
            - If the request is missing a payload:
                {
                    "Message": "Missing payload."
                }
            - If the payload is incorrectly formatted:
                {
                    "Message": "Incorrect payload."
                }

    Example Response:
        - Successful password reset:
            {
                "Message": "Password successfully reset."
            }
    """

    # Reset the user's password using Cognito's confirm forgot password API
    cognito.confirm_forgot_password(
        validated_data["Username"],
        validated_data["ConfirmationCode"],
        validated_data["Password"]
    )

    # Return a success response with a 200 status code
    res = make_response({"Message": "Password successfully reset."}, 200)

    return res


@blueprint.route("/refresh", methods=["POST"])
@validate_schema(Base.refresh_schema)
def refresh(validated_data: Base.RefreshRequestType):
    """
    Refresh the user's Access Token using the Refresh Token.

    This endpoint allows the user to obtain a new Access Token by providing a 
    valid Refresh Token. Upon successful verification and refresh, the endpoint 
    returns a new Access Token in the response.

    Request Body:
        - AccessToken (str): The current (but potentially expired) Access Token.
        - RefreshToken (str): The Refresh Token used to generate a new Access
            Token.

    Responses:
        200 OK:
            - If the Access Token is successfully refreshed:
                {
                    "Message": "Access token successfully refreshed.",
                    "AccessToken": <New AccessToken>
                }

        401 Unauthorized:
            - If the required AccessToken or RefreshToken is missing:
                {
                    "Message": "access_token or refresh_token cookies are not
                               present."
                }

        500 Internal Server Error:
            - If there is an error verifying the token or refreshing the access
                token:
                {
                    "Message": "Error refreshing access token."
                }

    Example Response:
        - Successful refresh:
            {
                "Message": "Access token successfully refreshed.",
                "AccessToken": "new-access-token"
            }
    """
    access_token = validated_data["AccessToken"]

    # Attempt to extract claims from the Access Token using Cognito
    try:
        claim = cognito.get_claim_from_access_token(access_token)
    except Exception as e:
        return handle_server_error("Error refreshing access token.", 500, e)

    refresh_token = validated_data["RefreshToken"]

    # Attempt to refresh the tokens using Cognito
    try:
        auth_result = cognito.refresh(claim["username"], refresh_token)
    except Exception as e:
        return handle_server_error("Error refreshing access token.", 403, e)

    # Attempt to retrieve the new Access Token from the Cognito response
    try:
        access_token = auth_result["AuthenticationResult"]["AccessToken"]
    except Exception as e:
        return handle_server_error("Failure retrieving access token.", 500, e)

    # Attempt to verify the new Access Token
    try:
        cognito.get_claim_from_access_token(access_token)
    except Exception as e:
        return handle_server_error("Failure verifying access token.", 500, e)

    # Prepare the success response with the new Access Token
    response = make_response(
        {
            "Message": "Access token successfully refreshed.",
            "AccessToken": access_token
        },
        200
    )

    return response
