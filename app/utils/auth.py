from functools import wraps
import requests

from flask import current_app, g, jsonify, request
from jose import jwt


def get_jwks():
    response = requests.get(current_app.config["COGNITO_JWKS_URL"])
    response.raise_for_status()
    return response.json()


def decode_token(token: str):
    try:
        # Retrieve JWKS
        jwks = get_jwks()
        headers = jwt.get_unverified_headers(token)
        kid = headers["kid"]

        # Find the key with the matching kid
        key = next(key for key in jwks["keys"] if key["kid"] == kid)

        # Decode and verify the token
        region = current_app.config["COGNITO_REGION"]
        userpool_id = current_app.config["COGNITO_USERPOOL_ID"]
        decoded = jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            audience=current_app.config["COGNITO_APP_CLIENT_ID"],
            issuer=f"https://cognito-idp.{region}.amazonaws.com/{userpool_id}"
        )

        return decoded

    except Exception as e:
        print(f"Token decoding failed: {e}")
        return None


def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get("access_token")
        if not token:
            return jsonify({"message": "Unauthorized"}), 401

        decoded = decode_token(token)
        if not decoded:
            return jsonify({"message": "Unauthorized"}), 401

        # Store decoded token in Flask"s g for use within routes
        g.user = decoded

        return f(*args, **kwargs)

    return decorated_function
