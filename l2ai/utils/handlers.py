import logging

logger = logging.getLogger(__name__)


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
