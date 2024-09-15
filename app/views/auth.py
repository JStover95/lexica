import requests

from flask import Blueprint, current_app, jsonify, make_response, request

from app.utils.auth import decode_token

blueprint = Blueprint("auth", __name__)


@blueprint.route("/refresh-token", methods=["POST"])
def refresh_token():
    """
    Refreshes the access token using the refresh token stored in cookies.

    This endpoint checks for the presence of a refresh token in the cookies. If
    the refresh token is valid, it requests new tokens from the AWS Cognito
    token URL and updates the `access_token` cookie. If the refresh token is
    missing or invalid, it returns a 401 Unauthorized response.

    Returns:
        Response: A JSON response indicating whether the token was successfully
        refreshed or an error message if the refresh process fails.
        TODO: Describe the response body's attributes.

    HTTP Status:
        - 200 OK: Token refreshed successfully.
        - 400 Bad Request: Error with the token exchange or invalid refresh
        token.
        - 401 Unauthorized: Refresh token not found in cookies.
    """
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        return jsonify({"message": "Unauthorized"}), 401

    # Request new tokens
    token_url = f"https://{current_app.config["COGNITO_DOMAIN"]}/oauth2/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    body = {
        "grant_type": "refresh_token",
        "client_id": current_app.config["COGNITO_APP_CLIENT_ID"],
        "refresh_token": refresh_token
    }

    response = requests.post(token_url, headers=headers, data=body)
    token_data = response.json()

    if "access_token" in token_data:
        # Update token cookies
        response = make_response(jsonify({"message": "Token refreshed"}))
        response.set_cookie(
            "access_token",
            token_data["access_token"],
            httponly=True,
            secure=True
        )

        return response

    return jsonify({"error": token_data}), 400


@blueprint.route("/token-exchange", methods=["POST"])
def token_exchange():
    """
    Exchanges an authorization code for access and refresh tokens.

    This endpoint receives an authorization code as a POST request, exchanges it
    with AWS Cognito for an access token and a refresh token, and sets these
    tokens as HttpOnly, Secure cookies. If the code is missing or the token
    exchange fails, it returns an error message.

    Request Body (JSON):
        - code (str): The authorization code provided by the AWS Cognito OAuth2
        flow.

    Returns:
        Response: A JSON response indicating the success of the login and the
        setting of cookies.
        TODO: Describe the response body's attributes

    HTTP Status:
        - 200 OK: Tokens successfully exchanged and cookies set.
        - 400 Bad Request: Missing authorization code or error during token
        exchange.
    """

    data = request.json
    code = data.get("code")

    if not code:
        return jsonify({"error": "Authorization code not provided"}), 400

    # Exchange code for tokens
    token_url = f"https://{current_app.config["COGNITO_DOMAIN"]}/oauth2/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    body = {
        "grant_type": "authorization_code",
        "client_id": current_app.config["COGNITO_APP_CLIENT_ID"],
        "redirect_uri": current_app.config["COGNITO_REDIRECT_URI"],
        "code": code
    }

    response = requests.post(token_url, headers=headers, data=body)
    token_data = response.json()

    if "access_token" in token_data:
        # Set HttpOnly Secure cookie
        response = make_response({"message": "Logged in"}, 200)
        response.set_cookie(
            "access_token",
            token_data["access_token"],
            httponly=True,
            secure=True
        )

        response.set_cookie(
            "refresh_token",
            token_data["refresh_token"],
            httponly=True,
            secure=True
        )

        return response

    return jsonify({"error": token_data}), 400


@blueprint.route("/verify-token", methods=["POST"])
def verify_token():
    """
    Verifies the validity of the access token stored in cookies.

    This endpoint retrieves the access token from the cookies and verifies it by
    decoding it using AWS Cognito's public keys. If the token is valid, it
    returns the decoded token information. If the token is invalid or expired,
    it returns a 401 response.

    Returns:
        Response: A JSON response indicating whether the token is valid, and if
        so, it includes the user's information.
        - messge (str): A message indicating the token's stats (Access token not
        found, Token valid, or Token invalid or expired)

    HTTP Status:
        - 200 OK: Token is valid, and user information is returned.
        - 401 Unauthorized: Access token is missing, invalid, or expired.
    """
    access_token = request.cookies.get("access_token")

    if not access_token:
        return jsonify({"message": "Access token not found"}), 401

    decoded = decode_token(access_token)
    if decoded:
        return jsonify({"message": "Token valid", "user": decoded}), 200

    return jsonify({"message": "Token invalid or expired"}), 401

