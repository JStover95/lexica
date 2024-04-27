from base64 import b64encode
import os
from flask.testing import FlaskClient
from werkzeug.test import TestResponse


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
    res = client.post("/login", headers=headers)

    return res


def initialize_cognito_test_environment():

    # import app after initializing mock AWS to ensure no AWS clients are initialized
    from l2ai.collections import users
    from l2ai.extensions import cognito

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

    try:
        cognito.user_pool_id = res["UserPool"]["Id"]

    except KeyError:
        raise RuntimeError("Error retrieving UserPoolId.")

    res = cognito.client.create_user_pool_client(
        UserPoolId=cognito.user_pool_id,
        ClientName="TestAppClient",
        GenerateSecret=True
    )

    try:
        cognito.client_id = res["UserPoolClient"]["ClientId"]
        cognito.client_secret = res["UserPoolClient"]["ClientSecret"]
    
    except KeyError:
        raise RuntimeError("Error retrieving UserPoolClient Id or Secret.")

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
