from base64 import b64encode
from flask.testing import FlaskClient
from werkzeug.test import TestResponse


def login(client: FlaskClient, username: str, password: str) -> TestResponse:
    cred = b64encode(f"{username}:{password}".encode())
    headers = {"Authorization": "Basic %s" % cred.decode()}
    res = client.post("/login", headers=headers)

    return res
