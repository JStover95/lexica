from base64 import b64encode
import os
from flask.testing import FlaskClient
from werkzeug.test import TestResponse

SIGNUP_USERNAME = "signup@email.com"
SIGNUP_PASSWORD = "Signup!@34"
CREATE_USERNAME = "create@email.com"
CREATE_PASSWORD = "Create!@34"


def login(client: FlaskClient, username: str, password: str) -> TestResponse:
    cred = b64encode(f"{username}:{password}".encode())
    headers = {"Authorization": "Basic %s" % cred.decode()}
    res = client.post("/login", headers=headers)

    return res


def initialize_cognito_test_environment():

    # import app after initializing mock AWS to ensure no AWS clients are initialized
    from l2ai.collections import User, users
    from l2ai.extensions import cognito

    user = users.find_one({"username": SIGNUP_USERNAME})
    if user is None:
        users.insert_one({"username": SIGNUP_USERNAME})

    user = users.find_one({"username": CREATE_USERNAME})
    if user is None:
        users.insert_one({"username": CREATE_USERNAME})

    res = cognito.client.create_user_pool(
        PoolName="TestUserPool",
        AliasAttributes=["email"],
        UsernameAttributes=["email"],
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
        Username=SIGNUP_USERNAME,
        Password=SIGNUP_PASSWORD
    )

    cognito.client.admin_confirm_sign_up(
        UserPoolId=cognito.user_pool_id,
        Username=SIGNUP_USERNAME
    )

    cognito.client.admin_create_user(
        UserPoolId=cognito.user_pool_id,
        Username=CREATE_USERNAME,
        TemporaryPassword=CREATE_PASSWORD
    )
