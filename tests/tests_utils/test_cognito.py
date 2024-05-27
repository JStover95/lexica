from flask import make_response
from l2ai.extensions import cognito
from l2ai.utils.cognito import set_access_cookies
from tests.utils import Fake


def test_set_access_cookies(client):
    auth_result = cognito.login(Fake.username(0), Fake.password(0))

    assert auth_result is not False

    response = make_response("foo", 200)
    set_access_cookies(response, auth_result)

    print(response.headers)
