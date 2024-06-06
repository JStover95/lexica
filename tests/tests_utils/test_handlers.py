from flask.testing import FlaskClient
from l2ai.utils.handlers import handle_server_error
from l2ai.utils.logging import logger


def test_handle_client_error():
    logger.info("Test for handle_client_error not implemented.")


def test_handle_server_error(client: FlaskClient):
    res = None

    try:
        raise Exception("Error")
    except Exception as e:
        msg = "An error has occured"
        res = handle_server_error(msg, 500, e)

    assert res is not None
    assert res.status_code == 500
    assert res.json is not None
    assert "Message" in res.json
    assert res.json["Message"] == msg
