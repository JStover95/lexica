import os
from typing import Generator
from flask.testing import FlaskClient
from moto import mock_aws
import pytest
from tests.utils import initialize_cognito_test_environment


@pytest.fixture
def client() -> Generator[FlaskClient, None, None]:
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"

    with mock_aws():

        # import app after initializing mock AWS to ensure no AWS clients are initialized
        from l2ai.app import create_app

        app = create_app(testing=True)
        initialize_cognito_test_environment()

        with app.app_context():
            with app.test_client() as client:
                yield client
