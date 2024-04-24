import os
from typing import Generator
import boto3
import dotenv
from flask import Flask
from flask.testing import FlaskClient
from moto import mock_aws
import pytest
from l2ai.app import create_app

dotenv.load_dotenv()


@pytest.fixture
def app() -> Generator[Flask, None, None]:
    with mock_aws():
        app = create_app(testing=True)
        with app.app_context():
            yield app


@pytest.fixture
def client(app: Flask) -> Generator[FlaskClient, None, None]:
    with app.test_client() as client:
        yield client
