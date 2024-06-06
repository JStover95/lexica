from base64 import b64encode
from typing import Any
from flask.testing import FlaskClient
from werkzeug.test import TestResponse
from werkzeug import Response
# from l2ai.collections import users
from l2ai.utils.cognito import Cognito


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
    access_token_cookie = get_cookie_from_response(res, "access_token")
    refresh_token_cookie = get_cookie_from_response(res, "refresh_token")
    client.set_cookie(**access_token_cookie)
    client.set_cookie(**refresh_token_cookie)

    return res


def initialize_cognito_test_environment(cognito: Cognito):

    # avoid importing before moto.mock_aws is called
    from l2ai.collections import users

    user = users.find_one({"username": Fake.username(0)})
    if user is None:
        users.insert_one({"username": Fake.username(0)})

    user = users.find_one({"username": Fake.username(1)})
    if user is None:
        users.insert_one({"username": Fake.username(1)})

    user = users.find_one({"username": Fake.username(2)})
    if user is None:
        users.insert_one({"username": Fake.username(2)})

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
