import os
from flask.testing import FlaskClient
import pytest
from mypy_boto3_cognito_idp.type_defs import InitiateAuthResponseTypeDef
from tests.utils import login

COGNITO_USERNAME = os.getenv("COGNITO_USERNAME")
COGNITO_PASSWORD = os.getenv("COGNITO_PASSWORD")


# @pytest.mark.parametrize(
#     "username,password",
#     [
#         ("fake@email.com", "fakepassword"),
#         (COGNITO_USERNAME, COGNITO_PASSWORD)
#     ]
# )
# def test_login(client: FlaskClient, username: str, password: str):
#     res = login(client, username, password)

#     if res.json is not None:
#         data: InitiateAuthResponseTypeDef = res.json
