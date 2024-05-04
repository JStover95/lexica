from functools import wraps
import traceback
from typing import Mapping, TypedDict
from flask import make_response, request
from jsonschema import validate, ValidationError
from mypy_boto3_cognito_idp.literals import ChallengeNameType
from l2ai.utils.handlers import handle_server_error


def validate_schema(schema):
    def wrapped_func(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if request.json is None:
                return make_response({"Message": "Missing payload."}, 401)
            try:
                validate(request.json, schema)
            except ValidationError as e:
                return handle_server_error("Invalid paylod.", 401, e)

            return f(*args, validated_data=request.json, **kwargs)

        return wrapper

    return wrapped_func


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
