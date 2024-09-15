from functools import wraps
import requests

from flask import current_app, g, jsonify, request
from jose import jwt


def get_jwks():
    """
    Fetches the JSON Web Key Set (JWKS) from AWS Cognito.

    This function retrieves the public keys from the configured AWS Cognito JWKS
    URL. These keys are used to verify the signature of JWT tokens issued by the
    Cognito user pool.

    Returns:
        dict: A dictionary containing the JWKS (public keys) from AWS Cognito.

    Raises:
        HTTPError: If the HTTP request to the JWKS URL fails.
    """
    response = requests.get(current_app.config["COGNITO_JWKS_URL"])
    response.raise_for_status()
    return response.json()


def decode_token(token: str):
    """
    Decodes and verifies a JWT access token using AWS Cognito's public keys.

    This function retrieves the JWKS from AWS Cognito, locates the appropriate
    key based on the token's "kid" (key ID), and verifies the token's signature
    and claims (audience and issuer).

    Args:
        token (str): The JWT access token to decode and verify.

    Returns:
        dict: The decoded token payload if verification is successful.
        None: If the token is invalid or verification fails.

    Raises:
        Exception: If the token decoding or verification process encounters an
            error.
    """
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
    """
    A decorator to protect Flask routes, requiring valid JWT authentication.

    This function checks if the request contains a valid JWT access token in the
    cookies. If the token is present and valid, it decodes the token and stores
    the user information in Flask's `g` object for use within the route. If the
    token is missing or invalid, it returns a 401 Unauthorized response.

    Args:
        f (function): The Flask view function to be protected by the
            authentication check.

    Returns:
        function: A wrapped function that requires JWT authentication.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get("access_token")
        if not token:
            return jsonify({"message": "Unauthorized"}), 401

        decoded = decode_token(token)
        if not decoded:
            return jsonify({"message": "Unauthorized"}), 401

        # Store decoded token in Flask's g for use within routes
        g.user = decoded

        return f(*args, **kwargs)

    return decorated_function
