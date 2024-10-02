from functools import wraps
from typing import Mapping, TypedDict, NotRequired

from flask import make_response, request
from jsonschema import validate, ValidationError
from mypy_boto3_cognito_idp.literals import ChallengeNameType
from werkzeug.datastructures import MultiDict

from app.utils.handlers import handle_server_error


def validate_schema(schema):
    """
    A decorator function to enforce JSON payload validation for Flask endpoints
    using the jsonschema library.

    This decorator checks if the incoming request contains a JSON payload and
    validates it against the provided schema. If the payload is missing or
    invalid, it returns a 401 Unauthorized response with an appropriate error
    message.

    Args:
        - schema (dict): The JSON schema to validate the incoming request data
        against.

    Returns:
        function: The wrapped Flask route function, which is executed if the
        payload is valid. The validated JSON data is passed to the route
        function via the `validated_data` keyword argument.

    Example usage:
        @app.route('/example', methods=['POST'])
        @validate_schema(example_schema)
        def example_endpoint(validated_data):
            # Use the validated_data here
            pass
    """
    def wrapped_func(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # Check if the incoming request has a JSON payload
            if request.json is None:
                return make_response({"Message": "Missing payload."}, 401)
            try:
                # Validate the request JSON data against the provided schema
                validate(request.json, schema)
            except ValidationError as e:
                # Handle validation errors by returning a 401 Unauthorized response
                return handle_server_error("Invalid paylod.", 401, e)

            # If validation is successful, pass the validated data to the route function
            return f(*args, validated_data=request.json, **kwargs)

        return wrapper

    return wrapped_func


def validate_parameters(schema):
    def wrapped_func(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # Check if the incoming request has a JSON payload
            if not request.args.to_dict():
                return make_response({"Message": "Missing parameters."}, 401)
            try:
                # Validate the request JSON data against the provided schema
                validate(request.args.to_dict(), schema)
            except ValidationError as e:
                # Handle validation errors by returning a 401 Unauthorized response
                return handle_server_error("Invalid parameters.", 401, e)

            # If validation is successful, pass the validated data to the route function
            return f(*args, validated_params=request.args.to_dict(), **kwargs)

        return wrapper

    return wrapped_func


class API:
    InferRequestType = TypedDict(
        "InferRequestType",
        {
            "Query": str,
            "Context": NotRequired[str],
        }
    )

    infer_schema = {
        "type": "object",
        "properties": {
            "Query": {"type": "string"},
            "Context": {"type": "string"},
        },
        "required": [
            "Query",
        ],
    }

    ContentRequestType = TypedDict(
        "ContentRequestType",
        {
            "q": str
        }
    )

    content_schema = {
        "type": "object",
        "properties": {
            "q": {"type": "string"}
        },
        "required": [
            "q"
        ]
    }


class Base:
    ChallengeRequestType = TypedDict(
        "ChallengeRequestType",
        {
            "Username": str,
            "ChallengeName": ChallengeNameType,
            "Session": str,
            "ChallengeResponses": Mapping[str, str]
        }
    )

    challenge_schema = {
        "type": "object",
        "properties": {
            "Username": {"type": "string"},
            "ChallengeName": {"type": "string"},
            "Session": {"type": "string"},
            "ChallengeResponses": {
                "type": "object",
                "properties": {
                    "USERNAME": {"type": "string"},
                    "NEW_PASSWORD": {"type": "string"},
                    "SMS_MFA_CODE": {"type": "string"},
                    "PASSWORD_CLAIM_SIGNATURE": {"type": "string"},
                    "PASSWORD_CLAIM_SECRET_BLOCK": {"type": "string"},
                    "TIMESTAMP": {"type": "string"},
                    "ANSWER": {"type": "string"},
                    "NEW_PASSWORD": {"type": "string"},
                    "SOFTWARE_TOKEN_MFA_CODE": {"type": "string"},
                    "DEVICE_KEY": {"type": "string"},
                    "SRP_A": {"type": "string"},
                    "SESSION": {"type": "string"},
                },
                "required": ["USERNAME"]
            }
        },
        "required": [
            "Username",
            "ChallengeName",
            "Session",
            "ChallengeResponses"
        ]
    }

    LogoutRequestType = TypedDict(
        "LogoutRequestType",
        {
            "Username": str
        }
    )

    logout_schema = {
        "type": "object",
        "parameters": {
            "Username": {"type": "string"}
        },
        "required": ["Username"]
    }

    ForgotPasswordRequestType = TypedDict(
        "ForgotPasswordRequestType",
        {
            "Username": str
        }
    )

    forgot_password_schema = {
        "type": "object",
        "parameters": {
            "Username": {"type": "string"}
        },
        "required": ["Username"]
    }

    ConfirmForgotPasswordRequestType = TypedDict(
        "ConfirmForgotPasswordRequestType",
        {
            "Username": str,
            "ConfirmationCode": str,
            "Password": str
        }
    )

    confirm_forgot_password_schema = {
        "type": "object",
        "parameters": {
            "Username": {"type": "string"},
            "ConfirmationCode": {"type": "number"},
            "Password": {"type": "string"},
        },
        "required": ["Username", "ConfirmationCode", "Password"]
    }

    RefreshRequestType = TypedDict(
        "RefreshRequestType",
        {
            "AccessToken": str,
            "RefreshToken": str
        }
    )

    refresh_schema = {
        "type": "object",
        "parameters": {
            "AccessToken": {"type": "string"},
            "RefreshToken": {"type": "string"}
        },
        "required": ["AccessToken", "RefreshToken"]
    }
