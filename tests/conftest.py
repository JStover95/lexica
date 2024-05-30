import os
from typing import Generator
from flask import Flask, make_response
from flask.testing import FlaskClient
from moto import mock_aws
import pytest
from l2ai.utils.cognito import Cognito
from l2ai.utils.logging import logger
from tests.utils import initialize_cognito_test_environment


@pytest.fixture
def cognito() -> Generator[Cognito, None, None]:
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"

    with mock_aws():

        # import Cognito after initializing mock AWS to ensure no AWS clients are initialized
        from l2ai.extensions import cognito
        initialize_cognito_test_environment(cognito)

        yield cognito


@pytest.fixture
def app(cognito: Cognito) -> Generator[Flask, None, None]:

    # import app after initializing mock AWS to ensure no AWS clients are initialized
    from l2ai.app import create_app

    app = create_app(testing=True)
    with app.app_context():

        # create a protected route for testing
        @app.route("/protected")
        @cognito.login_required
        def protected():
            return make_response("foo", 200)
        
        yield app


@pytest.fixture
def client(app: Flask) -> Generator[FlaskClient, None, None]:
    with app.test_client() as client:
        yield client
