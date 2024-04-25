from base64 import b64encode
import os
from flask.testing import FlaskClient
from werkzeug.test import TestResponse


def login(client: FlaskClient, username: str, password: str) -> TestResponse:
    cred = b64encode(f"{username}:{password}".encode())
    headers = {"Authorization": "Basic %s" % cred.decode()}
    res = client.post("/login", headers=headers)

    return res


def initialize_cognito_test_environment():

    # import app after initializing mock AWS to ensure no AWS clients are initialized
    from l2ai.extensions import cognito

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
    
    username = os.getenv("COGNITO_USERNAME")
    password = os.getenv("COGNITO_PASSWORD")

    if not (username and password):
        raise ValueError("Environment variables COGNITO_USERNAME and COGNITO_PASSWORD must be set.")

    else:
        cognito.client.sign_up(
            ClientId=cognito.client_id,
            Username=username,
            Password=password
        )

    cognito.client.admin_confirm_sign_up(
        UserPoolId=cognito.user_pool_id, Username=username
    )
