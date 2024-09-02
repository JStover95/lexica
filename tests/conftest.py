import os
from typing import Generator
from flask import Flask
from flask.testing import FlaskClient
from moto import mock_aws
import pytest
from app.utils.cognito import Cognito
from app.utils.mongo import Mongo
from tests.utils import (
    initialize_app_test_environment,
    initialize_cognito_test_environment,
    initialize_mongo_test_environment
)

os.environ["MONGO_NAME"] = "testing"
os.environ["COGNITO_CLIENT_ID"] = "testing"
os.environ["COGNITO_CLIENT_SECRET"] = "testing"


@pytest.fixture
def cognito() -> Generator[Cognito, None, None]:
    with mock_aws():
        from app.extensions import cognito
        initialize_cognito_test_environment(cognito)

        yield cognito


@pytest.fixture
def mongo(cognito: Cognito) -> Generator[Mongo, None, None]:
    from app.extensions import mongo
    initialize_mongo_test_environment(mongo)
    yield mongo


@pytest.fixture
def app(cognito: Cognito, mongo: Mongo) -> Generator[Flask, None, None]:
    from app.app import create_app

    app = create_app(testing=True)
    initialize_app_test_environment(app, cognito)
    with app.app_context():
        yield app


@pytest.fixture
def client(app: Flask) -> Generator[FlaskClient, None, None]:
    with app.test_client() as client:
        yield client
