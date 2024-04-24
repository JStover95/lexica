import logging

logger = logging.getLogger(__name__)


def handle_client_error(e):
    try:
        code = e.response["Error"]["Code"]

    except KeyError:
        code = ""

    try:
        message = e.response["Error"]["Message"]

    except KeyError:
        message = ""

    logger.error("Error Code %s: %s", code, message)