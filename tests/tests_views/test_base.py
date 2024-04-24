import os
import dotenv
from flask.testing import FlaskClient
import pytest
from mypy_boto3_cognito_idp.type_defs import InitiateAuthResponseTypeDef
from l2ai.extensions import Cognito
from tests.utils import login

COGNITO_USERNAME = os.getenv("COGNITO_USERNAME")
COGNITO_PASSWORD = os.getenv("COGNITO_PASSWORD")


@pytest.mark.parametrize(
    "email,password",
    [
        # ("fake@email.com", "fakepassword"),
        (os.getenv("COGNITO_USERNAME"), os.getenv("COGNITO_PASSWORD"))
    ]
)
def test_login(client: FlaskClient, email: str, password: str):
    res = login(client, email, password)

    if res.json is not None:
        data: InitiateAuthResponseTypeDef = res.json
        print(data)
