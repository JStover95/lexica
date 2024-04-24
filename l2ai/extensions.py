from base64 import b64encode
from hashlib import sha256
import hmac
import logging
import os
import boto3
from botocore.exceptions import ClientError
from flask import Flask
from flask_socketio import SocketIO
from moto import mock_aws
import pymongo
from l2ai.utils.handlers import handle_client_error

logger = logging.getLogger(__name__)


class Cognito():
    def __init__(self):
        self.client = boto3.client("cognito-idp")
        self.user_pool_id: None | str = None
        self.client_id: None | str = None
        self.client_secret: None | str = None

    def init_app(self, app: Flask):
        if not app.config["TESTING"]:
            self.user_pool_id = os.getenv("COGNITO_USERPOOL_ID")
            self.client_id = os.getenv("COGNITO_CLIENT_ID")
            self.client_secret = os.getenv("COGNITO_CLIENT_SECRET")

        else:
            res = self.client.create_user_pool(PoolName="TestUserPool")

            try:
                self.user_pool_id = res["UserPool"]["Id"]

            except KeyError:
                raise Exception
            
            res = self.client.create_user_pool_client(
                UserPoolId=self.user_pool_id,
                ClientName="TestAppClient",
                GenerateSecret=True
            )

            try:
                self.client_id = res["UserPoolClient"]["ClientId"]
                self.client_secret = res["UserPoolClient"]["ClientSecret"]
            
            except KeyError:
                raise Exception
            
            username = os.getenv("COGNITO_USERNAME")
            password = os.getenv("COGNITO_PASSWORD")
            email = os.getenv("COGNITO_EMAIL")

            if not (username and password and email):
                raise Exception

            self.client.sign_up(
                ClientId=self.client_id,
                Username=username,
                Password=password,
                UserAttributes=[
                    {"Name": "email", "Value": email}
                ]
            )

            self.client.admin_confirm_sign_up(
                UserPoolId=self.user_pool_id, Username=username
            )


    def _secret_hash(self, username: str):
        if self.client_secret is not None:
            key = self.client_secret.encode()

        else:
            raise Exception

        if self.client_id is not None:
            msg = bytes(username + self.client_id, "utf-8")

        else:
            raise Exception

        secret_key = hmac.new(key, msg, digestmod=sha256).digest()
        secret_hash = b64encode(secret_key).decode()

        return secret_hash

    def login(self, username: str, password: str):
        try:
            kwargs = {
                "AuthFlow": "ADMIN_USER_PASSWORD_AUTH",
                "AuthParameters": {
                    "USERNAME": username,
                    "PASSWORD": password,
                    "SECRET_HASH": self._secret_hash(username)
                },
                "ClientId": self.client_id,
                "UserPoolId": self.user_pool_id,
            }

            res = self.client.admin_initiate_auth(**kwargs)

        except ClientError as e:
            handle_client_error(e)
            raise Exception

        return res


class MongoDB():
    def __init__(self):
        self.app = None
        self.name = None
        self.host = None
        self.port = None
        self.username = None
        self.password = None

    def init_app(self, app: Flask):
        self.name = app.config["MONGO_NAME"]
        self.host = app.config["MONGO_HOST"]
        self.port = app.config["MONGO_PORT"]
        self.username  = app.config["MONGO_USERNAME"]
        self.password  = app.config["MONGO_PASSWORD"]

    @property
    def db(self):
        client = pymongo.MongoClient(
            self.host,
            self.port,
            username=self.username,
            password=self.password
        )

        if self.name is not None:
            return client[self.name]

        else:
            raise Exception  # TODO: fix exception


cognito = Cognito()
mongo = MongoDB()
socketio = SocketIO()
