from base64 import b64encode
from hashlib import sha256
import hmac
import logging
import os
import requests
import time
from typing import Dict, Literal
import boto3
from botocore.exceptions import ClientError
from jose import jwk, jwt
from jose.utils import base64url_decode
from mypy_boto3_cognito_idp.type_defs import InitiateAuthResponseTypeDef
from l2ai.utils.handlers import handle_client_error

logger = logging.getLogger(__name__)


class Cognito():
    keys_url = "https://cognito-idp.%s.amazonaws.com/%s/.well-known/jwks.json"

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

        self.keys = self.get_keys()

    def _secret_hash(self, username: str) -> str:
        if self.client_secret is not None:
            key = self.client_secret.encode()
        
        else:
            raise ValueError("Cognito._secret_hash was called when client_secret is None.")

        msg = bytes(username + self.client_id, "utf-8")
        secret_key = hmac.new(key, msg, digestmod=sha256).digest()
        secret_hash = b64encode(secret_key).decode()

        return secret_hash

    def get_keys(self) -> list[Dict[str, str]]:
        region = os.getenv("AWS_DEFAULT_REGION")
        url = self.keys_url % (region, self.user_pool_id)
        res = requests.get(url).json()

        return res["keys"]
    
    @staticmethod
    def _get_key_index(keys, kid):
        key_index = -1
        for i in range(len(keys)):
            if kid == keys[i]["kid"]:
                key_index = i
                break

        if key_index == -1:
            raise ValueError("Public key not found in jwks.json")

        else:
            return key_index

    def verify_token(self, token: str):
        headers = jwt.get_unverified_headers(token)
        kid = headers["kid"]

        # search for the kid in the downloaded public keys
        try:
            key_index = self._get_key_index(self.keys, kid)

        except ValueError:
            logger.warn("KID not found in AWS public keys. Re-downloading public keys and retrying.")
            self.keys = self.get_keys()
            key_index = self._get_key_index(self.keys, kid)

        # construct the public key
        public_key = jwk.construct(self.keys[key_index])

        # get the last two sections of the token, message and signature
        message, encoded_signature = str(token).rsplit(".", 1)

        # decode the signature
        decoded_signature = base64url_decode(encoded_signature.encode("utf-8"))

        # verify the signature
        if not public_key.verify(message.encode("utf8"), decoded_signature):
            raise ValueError("Signature verification failed.")

        claims = jwt.get_unverified_claims(token)

        # verify the token expiration
        if time.time() > claims["exp"]:
            raise ValueError("Token is expired.")

        # verify the clientId
        if claims["client_id"] != self.client_id:
            raise ValueError("Token was not issued for this audience")

        return claims

    def login(
            self,
            username: str,
            password: str
        ) -> InitiateAuthResponseTypeDef | Literal[False]:
        try:
            kwargs = {
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

            res = self.client.admin_initiate_auth(**kwargs)

        except ClientError as e:
            try:
                code = e.response["Error"]["Code"]

                if code == "NotAuthorizedException":
                    return False

            except Exception:
                pass

            handle_client_error(e)

        return res
