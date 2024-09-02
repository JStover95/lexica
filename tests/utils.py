from base64 import b64encode
import os
from typing import Any
from flask import Flask, make_response
from flask.testing import FlaskClient
from werkzeug.test import TestResponse
from werkzeug import Response
from app.utils.cognito import Cognito
from app.utils.logging import logger
from app.utils.mongo import Mongo


class Fake:
    usernames = ["foo@email.com", "bar@email.com", "baz@email.com", "qux@email.com"]
    passwords = ["Foo!@1234", "Bar!@1234", "Baz!@1234", "Qux!@1234"]

    @classmethod
    def username(cls, i: int) -> str:
        return cls.usernames[i]

    @classmethod
    def password(cls, i: int) -> str:
        return cls.passwords[i]


def login(client: FlaskClient, username: str, password: str) -> TestResponse:
    cred = b64encode(f"{username}:{password}".encode())
    headers = {"Authorization": "Basic %s" % cred.decode()}
    res = client.get("/login", headers=headers)

    # try:
    #     access_token_cookie = get_cookie_from_response(res, "access_token")
    #     refresh_token_cookie = get_cookie_from_response(res, "refresh_token")
    #     client.set_cookie(**access_token_cookie)
    #     client.set_cookie(**refresh_token_cookie)
    # except ValueError:
    #     pass

    return res


def initialize_app_test_environment(app: Flask, cognito: Cognito):
    @app.route("/protected")
    @cognito.login_required
    def protected():
        return make_response("Success", 200)


def initialize_mongo_test_environment(mongo: Mongo):
    if mongo.name != "testing":
        raise RuntimeError("Attempted to initialize test environment with real database. MONGO_NAME must be set to \"testing.\"")

    mongo.db["User"].drop()
    mongo.db["User"].insert_one({"username": Fake.username(0)})
    mongo.db["User"].insert_one({"username": Fake.username(1)})
    mongo.db["User"].insert_one({"username": Fake.username(2)})


def initialize_cognito_test_environment(cognito: Cognito):
    if os.environ["AWS_ACCESS_KEY_ID"] != "FOOBARKEY":
        raise RuntimeError("Attempted to initialize test environment with real AWS credentials. Ensure to only initialize the test environment in a mock_aws block.")

    res = cognito.client.create_user_pool(
        PoolName="TestUserPool",
        AliasAttributes=["email"],
        UsernameAttributes=["email"],
        AccountRecoverySetting={
            "RecoveryMechanisms": [
                {
                    "Priority": 1,
                    "Name": "verified_email"
                },
            ]
        }
    )

    if "Id" in res["UserPool"]:
        cognito.user_pool_id = res["UserPool"]["Id"]

    else:
        raise RuntimeError("Error retrieving UserPoolId.")

    res = cognito.client.create_user_pool_client(
        UserPoolId=cognito.user_pool_id,
        ClientName="TestAppClient",
        GenerateSecret=True
    )

    if "ClientId" in res["UserPoolClient"]:
        cognito.client_id = res["UserPoolClient"]["ClientId"]
    else:
        raise RuntimeError("Error retrieving Client ID.")

    if "ClientSecret" in res["UserPoolClient"]:
        cognito.client_secret = res["UserPoolClient"]["ClientSecret"]
    else:
        raise RuntimeError("Error retrieving Client Secret.")

    cognito.client.sign_up(
        ClientId=cognito.client_id,
        Username=Fake.username(0),
        Password=Fake.password(0)
    )

    cognito.client.admin_confirm_sign_up(
        UserPoolId=cognito.user_pool_id,
        Username=Fake.username(0)
    )

    cognito.client.admin_create_user(
        UserPoolId=cognito.user_pool_id,
        Username=Fake.username(1),
        TemporaryPassword=Fake.password(1)
    )

    cognito.client.sign_up(
        ClientId=cognito.client_id,
        Username=Fake.username(2),
        Password=Fake.password(2)
    )

    cognito.client.admin_confirm_sign_up(
        UserPoolId=cognito.user_pool_id,
        Username=Fake.username(2)
    )


def get_cookie_from_response(
        response: Response,
        cookie_name: str
    ) -> dict[str, Any]:
    cookie_headers = response.headers.getlist("Set-Cookie")

    for header in cookie_headers:
        attributes = header.split(";")

        if cookie_name in attributes[0]:
            cookie = {}

            # store the key and value of the first attribute separately to
            # easily pass to set_cookie
            key, value = attributes[0].split("=")
            cookie["key"] = key
            cookie["value"] = value

            for attr in attributes[1:]:
                split = attr.split("=")
                key = split[0].strip().lower()
                val = split[1] if len(split) > 1 else True
                cookie[key] = val

            return cookie

    raise ValueError("Cookie %s not found." % cookie_name)
