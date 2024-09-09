import requests

from flask import Blueprint, current_app, jsonify, make_response, request

from app.utils.auth import decode_token

blueprint = Blueprint("auth", __name__)


@blueprint.route("/refresh-token", methods=["POST"])
def refresh_token():
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
        response.set_cookie("access_token", token_data["access_token"], httponly=True, secure=True)
        return response
    else:
        return jsonify({"error": token_data}), 400


@blueprint.route("/token-exchange", methods=["POST"])
def token_exchange():
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
        response.set_cookie("access_token", token_data["access_token"], httponly=True, secure=True)
        response.set_cookie("refresh_token", token_data["refresh_token"], httponly=True, secure=True)
        return response
    else:
        return jsonify({"error": token_data}), 400


@blueprint.route("/verify-token", methods=["POST"])
def verify_token():
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")

    if not access_token:
        return jsonify({"message": "Access token not found"}), 401

    decoded = decode_token(access_token)
    if decoded:
        return jsonify({"message": "Token valid", "user": decoded}), 200

    return jsonify({"message": "Token invalid or expired"}), 401

