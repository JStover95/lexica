from base64 import b64encode
from hashlib import sha256
import hmac
import logging
import os
import boto3
from botocore.exceptions import ClientError
from mypy_boto3_cognito_idp.type_defs import InitiateAuthResponseTypeDef
from l2ai.utils.handlers import handle_client_error

logger = logging.getLogger(__name__)


class Cognito():
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

    def _secret_hash(self, username: str) -> str:
        if self.client_secret is not None:
            key = self.client_secret.encode()
        
        else:
            raise ValueError("Cognito._secret_hash was called when client_secret is None.")

        msg = bytes(username + self.client_id, "utf-8")
        secret_key = hmac.new(key, msg, digestmod=sha256).digest()
        secret_hash = b64encode(secret_key).decode()

        return secret_hash

    def login(
            self,
            username: str,
            password: str
        ) -> InitiateAuthResponseTypeDef:
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
            handle_client_error(e)

        return res
