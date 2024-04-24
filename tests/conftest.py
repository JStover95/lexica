import os
from typing import Generator
import boto3
from flask import Flask
from flask.testing import FlaskClient
from moto import mock_aws
import pytest
from l2ai.app import create_app
from l2ai.extensions import cognito


def initialize_cognito_test_environment():
    res = cognito.client.create_user_pool(PoolName="TestUserPool")

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
    email = os.getenv("COGNITO_EMAIL")

    if not (username and password and email):
        raise ValueError("Environment variables COGNITO_USERNAME, COGNITO_PASSWORD, and COGNITO_EMAIL must be set.")

    else:
        cognito.client.sign_up(
            ClientId=cognito.client_id,
            Username=username,
            Password=password,
            UserAttributes=[
                {"Name": "email", "Value": email}
            ]
        )

    cognito.client.admin_confirm_sign_up(
        UserPoolId=cognito.user_pool_id, Username=username
    )


@pytest.fixture
def client() -> Generator[FlaskClient, None, None]:
    with mock_aws():
        app = create_app(testing=True)
        initialize_cognito_test_environment()

        with app.app_context():
            with app.test_client() as client:
                yield client
