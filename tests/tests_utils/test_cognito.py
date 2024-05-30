from base64 import b64encode
from hashlib import sha256
import hmac
from flask import Flask, make_response
from flask.testing import FlaskClient
import pytest
from l2ai.utils.cognito import Cognito, set_access_cookies
from l2ai.utils.logging import logger
from tests.utils import Fake, get_cookie_from_response, login


def test_set_access_cookies(cognito: Cognito, client: FlaskClient):
    auth_result = cognito.login(Fake.username(0), Fake.password(0))

    assert auth_result is not False
    assert "AccessToken" in auth_result["AuthenticationResult"]
    assert "RefreshToken" in auth_result["AuthenticationResult"]

    response = make_response("foo", 200)
    set_access_cookies(response, auth_result)
    access_token_cookie = get_cookie_from_response(response, "access_token")
    refresh_token_cookie = get_cookie_from_response(response, "refresh_token")

    assert auth_result["AuthenticationResult"]["AccessToken"] == access_token_cookie["value"]
    assert auth_result["AuthenticationResult"]["RefreshToken"] == refresh_token_cookie["value"]


def test_set_access_cookies_runtime_error(cognito: Cognito, client: FlaskClient):
    auth_result = cognito.login(Fake.username(0), Fake.password(0))

    assert auth_result is not False

    # delete "AccessToken" to emulate receiving an auth challenge
    del auth_result["AuthenticationResult"]["AccessToken"]
    response = make_response("foo", 200)

    with pytest.raises(RuntimeError):
        set_access_cookies(response, auth_result)


class TestCognito:
    def test_secret_hash(self, cognito: Cognito):
        hash = cognito._secret_hash(Fake.username(0))

        assert cognito.client_secret is not None
        key = cognito.client_secret.encode()
        msg = bytes(Fake.username(0) + cognito.client_id, "utf-8")
        secret_key = hmac.new(key, msg, digestmod=sha256).digest()
        secret_hash = b64encode(secret_key).decode()

        assert hash == secret_hash

    def test_secret_hash_value_error(self, cognito: Cognito):
        cognito.client_secret = None

        with pytest.raises(ValueError):
            cognito._secret_hash(Fake.username(0))

    def test_get_public_keys(self, cognito: Cognito):
        keys = cognito.get_public_keys()

        # the test environment should have one key
        assert len(keys) == 1
        assert all(k in ["alg", "e", "kid", "kty", "n", "use"] for k in keys[0])

    def test_get_public_key_index(self, cognito: Cognito):

        # the test environment should have one key
        assert len(cognito.public_keys) == 1

        kid = cognito.public_keys[0]["kid"]
        key_index = cognito.get_public_key_index(kid)

        # the test environment should have one key, so the index will always be 0
        assert key_index == 0

    def test_get_public_key_index_value_error(self, cognito: Cognito):

        # the test environment should have one key
        assert len(cognito.public_keys) == 1

        with pytest.raises(ValueError):
            cognito.get_public_key_index("fake kid")

    def test_get_claim_from_access_token(self, cognito: Cognito):
        auth_result = cognito.login(Fake.username(0), Fake.password(0))

        assert auth_result is not False
        assert "AccessToken" in auth_result["AuthenticationResult"]

        token = auth_result["AuthenticationResult"]["AccessToken"]
        claim = cognito.get_claim_from_access_token(token)

        assert all(k in ["iss", "sub", "client_id", "token_use", "auth_time", "exp", "username"] for k in claim)
        assert claim["username"] == Fake.username(0)

    def test_get_claim_from_access_token_value_error(self, cognito: Cognito):
        logger.info("Test for raising a ValueError with Cognito.get_claim_from_access_token is not implemented.")

    def test_get_claim_from_access_token_invalid_token(self, cognito: Cognito):
        with pytest.raises(ValueError) as exc_info:
            cognito.get_claim_from_access_token("fake token")

        assert str(exc_info.value) == "Invalid token."

    def test_login_required(self, client: FlaskClient):
        res = login(client, Fake.username(0), Fake.password(0))
        res = client.get("/protected")
        assert res.status_code == 200

    def test_login_required_no_token(self, client: FlaskClient):
        res = client.get("/protected")
        assert res.status_code == 403

    def test_login_required_fake_token(self, client: FlaskClient):
        client.set_cookie("access_token", "fake token")
        res = client.get("/protected")
        assert res.status_code == 403

    def test_login_required_invalid_claim(self, client: FlaskClient):
        logger.info("Test for making an invalid claim with Cognito.login_required is not implemented.")
