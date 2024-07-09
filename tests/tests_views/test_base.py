from base64 import b64encode
from time import sleep
from flask.testing import FlaskClient
from l2ai.utils.cognito import Cognito
from tests.utils import Fake, get_cookie_from_response, logger, login


def test_login(client: FlaskClient):
    cred = b64encode(f"{Fake.username(0)}:{Fake.password(0)}".encode())
    headers = {"Authorization": "Basic %s" % cred.decode()}
    res = client.get("/login", headers=headers)

    assert res.status_code == 200
    assert res.json is not None
    assert "Message" in res.json
    assert res.json["Message"] == "Successful login."
    assert "AccessToken" in res.json
    assert "RefreshToken" in res.json

    headers = {"Authorization": "Bearer %s" % res.json["AccessToken"]}
    res = client.get("/protected", headers=headers)

    assert res.status_code == 200

    # access_token_cookie = get_cookie_from_response(res, "access_token")
    # refresh_token_cookie = get_cookie_from_response(res, "refresh_token")

    # assert access_token_cookie
    # assert refresh_token_cookie


def test_login_challenge(client: FlaskClient):
    cred = b64encode(f"{Fake.username(1)}:{Fake.password(1)}".encode())
    headers = {"Authorization": "Basic %s" % cred.decode()}
    res = client.get("/login", headers=headers)

    assert res.status_code == 200
    assert res.json is not None
    assert "Message" in res.json
    assert res.json["Message"] == "Challenge requested by server."
    assert all(x in res.json for x in ["ChallengeName", "Session", "ChallengeParameters"])


def test_login_no_credentials(client: FlaskClient):
    res = client.get("/login")

    assert res.status_code == 401
    assert res.json is not None
    assert "Message" in res.json
    assert res.json["Message"] == "Login credentials are required."


def test_login_invalid_auth_header(client: FlaskClient):
    cred = b64encode(f"fake auth header".encode())
    headers = {"Authorization": "Basic %s" % cred.decode()}
    res = client.get("/login", headers=headers)

    assert res.status_code == 401
    assert res.json is not None
    assert "Message" in res.json
    assert res.json["Message"] == "Error retrieving login credentials."


def test_login_invalid_credentials(client: FlaskClient):
    cred = b64encode(f"{Fake.username(0)}:{Fake.password(1)}".encode())
    headers = {"Authorization": "Basic %s" % cred.decode()}
    res = client.get("/login", headers=headers)

    assert res.status_code == 403
    assert res.json is not None
    assert "Message" in res.json
    assert res.json["Message"] == "Invalid login credentials."


def test_login_invalid_token(client: FlaskClient):
    logger.info("Test for base.login where token verification after successful login fails is not implemented.")


def test_challenge(client: FlaskClient):
    res = login(client, Fake.username(1), Fake.password(1))

    assert res.json is not None
    logger.info(res.json)

    body = {
        "Username": Fake.username(1),
        "ChallengeName": res.json["ChallengeName"],
        "Session": res.json["Session"],
        "ChallengeResponses": {
            "NEW_PASSWORD": Fake.password(2),
            "USERNAME": Fake.username(1)
        }
    }

    res = client.post("/challenge", json=body)

    assert res.status_code == 200
    assert res.json is not None
    assert "Message" in res.json
    assert res.json["Message"] == "Login successful."
    assert "AccessToken" in res.json
    assert "RefreshToken" in res.json

    headers = {"Authorization": "Bearer %s" % res.json["AccessToken"]}
    res = client.get("/protected", headers=headers)

    assert res.status_code == 200


def test_challenge_invalid_response(client: FlaskClient):
    logger.info("Test for base.challenge with an invalid response not implemented.")


def test_challenge_invalid_token(client: FlaskClient):
    logger.info("Test for base.challenge where token verification after successful login fails is not implemented.")


def test_logout(client: FlaskClient):
    logger.info("Test for base.logout not implemented.")


def test_forgot_password(client: FlaskClient):
    body = {"Username": Fake.username(0)}
    res = client.post("/forgot-password", json=body)

    assert res.status_code == 200
    assert res.json is not None
    assert "Message" in res.json
    assert res.json["Message"] == "Confirmation code sent successfully."
    assert "CodeDeliveryDetails" in res.json


def test_confirm_forgot_password(client: FlaskClient):
    body = {
        "Username": Fake.username(0),
        "ConfirmationCode": "1234",
        "Password": Fake.password(1)
    }

    res = client.post("/confirm-forgot-password", json=body)

    assert res.status_code == 200
    assert res.json is not None
    assert "Message" in res.json
    assert res.json["Message"] == "Password successfully reset."


def test_confirm_forgot_password_invalid_code(client: FlaskClient):
    logger.info("Test for base.confirm_forgot_password with invalid confirmation code not implemented.")


def test_refresh(cognito: Cognito, client: FlaskClient):
    res = login(client, Fake.username(0), Fake.password(0))
    # access_token_cookie = get_cookie_from_response(res, "access_token")
    access_token = res.json["AccessToken"]
    refresh_token = res.json["RefreshToken"]
    claim = cognito.get_claim_from_access_token(access_token)
    expiry = claim["exp"]

    sleep(1)
    body = {"AccessToken": access_token, "RefreshToken": refresh_token}
    res = client.post("/refresh", json=body)

    assert res.status_code == 200
    assert res.json is not None
    assert "Message" in res.json
    assert res.json["Message"] == "Access token successfully refreshed."
    assert "AccessToken" in res.json

    access_token = res.json["AccessToken"]
    headers = {"Authorization": "Bearer %s" % access_token}
    res = client.get("/protected", headers=headers)

    assert res.status_code == 200

    # access_token_cookie = get_cookie_from_response(res, "access_token")
    # access_token_cookie = get_cookie_from_response(res, "access_token")
    # claim = cognito.get_claim_from_access_token(access_token_cookie["value"])
    claim = cognito.get_claim_from_access_token(access_token)

    assert expiry < claim["exp"]


def test_refresh_invalid_token(client: FlaskClient):
    res = login(client, Fake.username(0), Fake.password(0))
    access_token = res.json["AccessToken"]
    body = {"AccessToken": access_token, "RefreshToken": "Fake Token"}
    res = client.post("/refresh", json=body)

    assert res.status_code == 403
    assert res.json is not None
    assert "Message" in res.json
    assert res.json["Message"] == "Error refreshing access token."


def test_connect(client: FlaskClient):
    logger.info("Test for base.connect not implemented.")


def test_disconnect(client: FlaskClient):
    logger.info("Test for base.disconnect not implemented.")
