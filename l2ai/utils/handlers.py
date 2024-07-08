from flask import make_response, Response
from botocore.exceptions import ClientError
from l2ai.utils.logging import logger


def handle_client_error(e: ClientError) -> None:
    """
    Handle AWS boto3 client errors. Get the error's code and message and create
    a log output.

    Args:
        e (ClientError)

    Raises:
        RuntimeError
    """
    try:
        code = e.response["Error"]["Code"]

    except KeyError:
        code = "N/A"

    try:
        message = e.response["Error"]["Message"]

    except KeyError:
        message = "N/A"

    logger.error("ClientError \"%s\": \"%s\"", code, message)


def handle_server_error(msg: str, code: int, e: Exception) -> Response:
    """
    Handle errors in server endpoints. Generate a logging message and return the
    a response with a message to the client.

    Args:
        msg (str): The message to return to the client
        code (int): The response code to return to the client (e.g., 401, 500)
        e (Exception)

    Returns:
        Response: The response to return to the client.
    """
    logger.error(msg)
    logger.exception(e)

    return make_response({"Message": msg}, code)
