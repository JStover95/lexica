from base64 import b64encode
from functools import wraps
from hashlib import sha256
import hmac
import os
import requests
import time
from typing import Any, Callable, Dict, Literal
import boto3
from botocore.exceptions import ClientError
from flask import make_response, request
from jose import jwk, jwt
from jose.exceptions import JWTError
from jose.utils import base64url_decode
from mypy_boto3_cognito_idp.type_defs import (
    ForgotPasswordResponseTypeDef,
    InitiateAuthResponseTypeDef,
)
from werkzeug import Response
from werkzeug.exceptions import BadRequestKeyError
from l2ai.utils.handlers import handle_client_error, handle_server_error
from l2ai.utils.logging import logger


def set_access_cookies(
        response: Response,
        auth_result: InitiateAuthResponseTypeDef,
    ) -> None:
    """
    Add the user's AccessToken and RefreshToken to a response using cookies.
    Cookies are always set to secure, HTTP only, and "Strict" same-site mode.

    Args:
        response (Response)
        auth_result (InitiateAuthResponseTypeDef): The authentication result
            returned from Cognito.login or Cognito.respond_to_challenge upon a
            successful login.

    Raises:
        RuntimeError: When the Access Token or Refresh Token are not found in
            auth_result. This may occur when Cognito.login returns with an
            authentication challenge.
    """
    try:
        access_token = auth_result["AuthenticationResult"]["AccessToken"]  # type: ignore
        refresh_token = auth_result["AuthenticationResult"]["RefreshToken"]  # type: ignore
    except KeyError:
        raise RuntimeError("Error retrieving Refresh Token from auth_result.")

    opts = {"secure": True, "httponly": True, "samesite": "Strict"}
    response.set_cookie("access_token", access_token, **opts)
    response.set_cookie("refresh_token", refresh_token, **opts)


class Cognito():
    """
    A helper class for working with the AWS Cognito Identity Provider client.

    This class will initialize using the following environment variables:
        - COGNITO_USERPOOL_ID
        - COGNITO_CLIENT_ID
        - COGNITO_CLIENT_SECRET

    A ValueError will be raised if the UserPoolId or ClientId are not found. If
    a ClientSecret is not set, a warning will be logged and all API calls will
    be made without a secret. Upon initialization, this class will automatically
    download the relevant public keys from a JWKS URI.

    Attributes:
        client (CognitoIdentityProviderClient)
        user_pool_id (str)
        client_id (str)
        client_secret (str | None)
        public_keys (list[Dict[str, str]]): a list of public keys as returned
            from the AWS JWKS URI when calling Cognito.get_public_keys

    Raises:
        ValueError: When the environment variables COGNITO_USERPOOL_ID or
            COGNITO_CLIENT_ID are not set.
    """

    # the format JWKS URI (https://cognito-idp.<Region>.amazonaws.com/<userPoolId>/.well-known/jwks.json)
    public_keys_url = "https://cognito-idp.%s.amazonaws.com/%s/.well-known/jwks.json"

    def __init__(self):
        self.client = boto3.client("cognito-idp")

        user_pool_id = os.getenv("COGNITO_USERPOOL_ID")
        if user_pool_id is None:
            raise ValueError("Environment variable COGNITO_USERPOOL_ID must be set.")
        else:
            self.user_pool_id = user_pool_id

        client_id = os.getenv("COGNITO_CLIENT_ID")
        if client_id is None:
            raise ValueError("Environment variable COGNITO_CLIENT_ID must be set.")
        else:
            self.client_id = client_id

        self.client_secret = os.getenv("COGNITO_CLIENT_SECRET")
        if self.client_secret is None:
            logger.warn("Environment variable COGNITO_CLIENT_SECRET is not set. A secret will not be used during user authentication")

        self.public_keys = self.get_public_keys()

    def _secret_hash(self, username: str) -> str:
        """
        Return a secret hash to be included on relevant API calls.

        Args:
            username (str): The relevant user's username.

        Raises:
            ValueError: If client_secret is None.

        Returns:
            str
        """
        if self.client_secret is not None:
            key = self.client_secret.encode()

        else:
            raise ValueError("Cognito._secret_hash was called when client_secret is None.")

        msg = bytes(username + self.client_id, "utf-8")
        secret_key = hmac.new(key, msg, digestmod=sha256).digest()
        secret_hash = b64encode(secret_key).decode()

        return secret_hash

    def get_public_keys(self) -> list[Dict[str, str]]:
        """
        Get public keys from the JWKS URI.

        Returns:
            list[Dict[str, str]]
        """
        region = os.getenv("AWS_DEFAULT_REGION")
        url = self.public_keys_url % (region, self.user_pool_id)
        res = requests.get(url).json()

        return res["keys"]
    
    def get_public_key_index(self, kid: str) -> int:
        """
        Given the Key ID of an Access Token, get the index of the public key
        that was used to encrpyt the Access Key.

        Args:
            kid (str): The Key ID of an Access Token

        Raises:
            ValueError: When the Key ID is not found in Cognito.public_keys

        Returns:
            int
        """
        key_index = -1
        for i in range(len(self.public_keys)):
            if kid == self.public_keys[i]["kid"]:
                key_index = i
                break

        if key_index == -1:
            raise ValueError("Public key not found.")

        else:
            return key_index

    def get_claim_from_access_token(self, token: str) -> Dict[str, Any]:
        """
        Validate and inspect a user's Access Token and return the decoded claim.
        See https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-using-tokens-verifying-a-jwt.html.

        If the Access Token's Key ID is not found in the public keys that were
        downloaded from the JWKS URI, the public keys will be redownloaded.

        Args:
            token (str): The user's Access Token

        Raises:
            ValueError: When verification of the Access Token fails. This can
                happen when validation of the token's signature fails, when the
                token is expired, or when the token was not issued for the
                current client (according to ClientId).

        Returns:
            Dict[str, str]: The Access Token's decoded claim.
        """
        try:
            headers = jwt.get_unverified_headers(token)

        except JWTError:
            raise ValueError("Invalid token.")

        kid = headers["kid"]

        # search for the Key ID in the downloaded public keys
        try:
            key_index = self.get_public_key_index(kid)

        # if it's not found, redownload keys and retry
        except ValueError:
            logger.warn("Key ID not found in public keys. Re-downloading public keys and retrying.")
            self.keys = self.get_public_keys()
            key_index = self.get_public_key_index(kid)

        # construct the public key
        public_key = jwk.construct(self.public_keys[key_index])

        # get the last two sections of the token, message and signature
        message, encoded_signature = str(token).rsplit(".", 1)

        # decode the signature
        decoded_signature = base64url_decode(encoded_signature.encode("utf-8"))

        # verify the signature
        if not public_key.verify(message.encode("utf8"), decoded_signature):
            raise ValueError("Signature verification failed.")

        claim = jwt.get_unverified_claims(token)

        # verify the token expiration
        if time.time() > claim["exp"]:
            raise ValueError("Token is expired.")

        # verify the clientId
        if claim["client_id"] != self.client_id:
            raise ValueError("Token was not issued for this client.")

        return claim

    def login_required(
            self,
            f: Callable[..., Any]
        ) -> Response | Callable[..., Any]:
        """
        Decorate a view function to restrict access to only users who have
        logged in and provide a valid Access Token. The Access Token must be
        saved in a cookie named access_token.
        
        In the case when a user's Access Token is not valid or when there is no
        Access Token present, this decorator will return a Response object that
        should be automatically handleded by the Flask client.

        Args:
            f (Callable[..., Any]): The wrapped function.

        Returns:
            Response | Callable[..., Any]
        """
        @wraps(f)
        def wrapper(*args, **kwargs):

            # get the Access Token from the access_token cookie.
            try:
                access_token = request.cookies["access_token"]

            # if no Access Token is present
            except BadRequestKeyError:
                return make_response({"Message": "Unauthorized request."}, 403)

            # make an API call to check whether the Access Token is valid
            try:
                self.client.get_user(AccessToken=access_token)

            # if an error occurs during the API call
            except ClientError as e:
                try:
                    code = e.response["Error"]["Code"]  # type: ignore

                    # if the Access Token is invalid
                    if code == "NotAuthorizedException":
                        return make_response({"Message": "Unauthorized request."}, 403)

                    # if any other reason, throw an exception to send a response
                    else:
                        raise Exception

                except KeyError as e:
                    msg = "An unexpected AWS client error occured during credential verification."
                    return handle_server_error(msg, 500, e)

            # inspect and validate the Access Token's claim
            try:
                self.get_claim_from_access_token(access_token)

            # if the claim is not valid
            except ValueError:  # TODO: make a separate exception for expired tokens
                return make_response({"Unauthorized request."}, 403)

            # if any other exception occured during validation
            except Exception as e:
                msg = "An unexpected error occured during credential verification."
                return handle_server_error(msg, 500, e)

            return f(*args, **kwargs)

        return wrapper

    def login(
            self,
            username: str,
            password: str
        ) -> InitiateAuthResponseTypeDef | Literal[False]:
        """
        Log a user in. Returns False when the user provides invalid credentials.

        Args:
            username (str)
            password (str)

        Returns:
            InitiateAuthResponseTypeDef | Literal[False]: Either the response
                from the AWS Cognito AdminInitiateUserAuth endpoint or False
                when the user provides invalid credentials.
        """
        kwargs: dict[str, Any] = {
            "AuthFlow": "ADMIN_USER_PASSWORD_AUTH",
            "AuthParameters": {
                "USERNAME": username,
                "PASSWORD": password,
            },
            "ClientId": self.client_id,
            "UserPoolId": self.user_pool_id,
        }

        if self.client_secret is not None:
            secret_hash = self._secret_hash(username)
            kwargs["AuthParameters"]["SECRET_HASH"] = secret_hash

        try:
            res = self.client.admin_initiate_auth(**kwargs)

        except ClientError as e:
            try:
                code = e.response["Error"]["Code"]  # type: ignore

                # when login was attempted with incorrect credentials
                if code == "NotAuthorizedException":
                    return False

            except KeyError:
                pass

            handle_client_error(e)
            res = False

        return res

    def respond_to_challenge(
            self,
            username: str,
            kwargs: dict[str, Any]
        ) -> InitiateAuthResponseTypeDef | Literal[False]:
        """
        Respond to an authorization challenge. Returns False when the challenge
        fails.

        Args:
            username (str)
            kwargs (dict[str, Any]): Keyword arguments to pass to 
                Client.respond_to_auth_challenge. See the AWS Cognito
                RespondToAuthChallenge endpoint documentation for more
                information:
                 - ChallengeName
                 - ChallengeResponses
                 - Session

        Returns:
            InitiateAuthResponseTypeDef | Literal[False]: The response from the
                AWS Cognito RespondToAuthChallenge endpoint or False if the
                challenge failed.
        """
        required_kwargs = ["ChallengeName", "ChallengeResponses", "Session"]

        for kwarg in required_kwargs:
            if kwarg not in kwargs:
                raise ValueError("Missing keyword argument for Cognito.respond_to_challenge: %s" % kwarg)

        kwargs["ClientId"] = self.client_id

        if self.client_secret is not None:
            secret_hash = self._secret_hash(username)
            kwargs["ChallengeResponses"]["SECRET_HASH"] = secret_hash

        try:
            res = self.client.respond_to_auth_challenge(**kwargs)

        except ClientError as e:
            try:
                code = e.response["Error"]["Code"]  # type: ignore

                # if the challenge failed
                if code == "NotAuthorizedException":
                    return False

            except KeyError:
                pass

            handle_client_error(e)

        return res

    def refresh(
            self,
            username: str,
            refresh_token: str,
        ) -> InitiateAuthResponseTypeDef:  # TODO: what happens when the refresh token is expired?
        """
        Generate a new Access Token using a Refresh Token. 

        Args:
            username (str)
            refresh_token (str)

        Returns:
            InitiateAuthResponseTypeDef: The response from the AWS Cognito
                AdminInitiateAuth endpoint.
        """
        kwargs: dict[str, Any] = {
            "AuthFlow": "REFRESH_TOKEN_AUTH",
            "AuthParameters": {"REFRESH_TOKEN": refresh_token},
            "ClientId": self.client_id,
            "UserPoolId": self.user_pool_id,
        }

        if self.client_secret is not None:
            secret_hash = self._secret_hash(username)
            kwargs["AuthParameters"]["SECRET_HASH"] = secret_hash

        try:
            res = self.client.admin_initiate_auth(**kwargs)

        except ClientError as e:
            handle_client_error(e)

        return res

    def sign_out(self, username: str) -> None:
        """
        Sign out a user.

        Args:
            username (str)
        """
        kwargs: dict[str, Any] = {
            "UserPoolId": self.user_pool_id,
            "Username": username
        }

        self.client.admin_user_global_sign_out(**kwargs)

    def forgot_password(self, username: str) -> ForgotPasswordResponseTypeDef:
        """
        Send a request for a password reset. This will either send an email or
        SMS message depending on the client's configuration.

        Args:
            username (str)

        Returns:
            ForgotPasswordResponseTypeDef: The response from the AWS
                ForgotPassword endpoint.
        """
        kwargs: dict[str, Any] = {
            "ClientId": self.client_id,
            "Username": username
        }

        if self.client_secret is not None:
            secret_hash = self._secret_hash(username)
            kwargs["SecretHash"] = secret_hash

        return self.client.forgot_password(**kwargs)
    
    def confirm_forgot_password(
            self,
            username: str,
            confirmation_code: str,
            password: str,
            kwargs: Dict[str, Any] | None = None
        ) -> None:
        """
        Using a confirmation code received by the user after calling
        Cognito.forgot_password, reset the user's password.

        Args:
            username (str)
            confirmation_code (str)
            password (str)
            kwargs (Dict[str, Any] | None, optional): Other arguments to pass to
                the AWS Cognito ConfirmForgotPassword enpoint. Defaults to None
        """
        kwargs = {
            "ClientId": self.client_id,
            "Username": username,
            "ConfirmationCode": confirmation_code,
            "Password": password,
            **(kwargs or {})
        }

        if self.client_secret is not None:
            secret_hash = self._secret_hash(username)
            kwargs["SecretHash"] = secret_hash

        self.client.confirm_forgot_password(**kwargs)
