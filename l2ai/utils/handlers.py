from flask import make_response, Response
import traceback
from l2ai.utils.logging import logger


def handle_client_error(e):
    try:
        code = e.response["Error"]["Code"]

    except KeyError:
        code = "N/A"

    try:
        message = e.response["Error"]["Message"]

    except KeyError:
        message = "N/A"

    logger.error("ClientError \"%s\": \"%s\"", code, message)
    raise RuntimeError("ClientError \"%s\": \"%s\"" % (code, message))


def handle_server_error(
        msg: str,
        code: int,
        e: Exception | None = None
    ) -> Response:
    if e is not None:
        logger.error(msg)
        logger.exception(e)
        exc = traceback.format_exception_only(e).pop().strip()
        res = {"Message": msg % {"exc": exc}}

    else:
        res = {"Message": msg}

    return make_response(res, code)
