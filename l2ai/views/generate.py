import logging
from flask import Blueprint

blueprint = Blueprint("generate", __name__)
logger = logging.getLogger(__name__)


@blueprint.route("/prompt", methods=["POST"])
def prompt():
    """
    Generate content using a prompt.

    Request syntax
    ---------------------
    {
        "Level": str,
        "Length": str,
        "Format": str,
        "Style": str,
        "Prompt": str
    }

    Response syntax (200)
    ---------------------
    {
        "Title": str,
        "Text": str
    }

    Response syntax (500)
    ---------------------
    {
        "Msg": a formatted traceback if an uncaught error was thrown
    }
    """
    pass


@blueprint.route("/image", methods=["POST"])
def image():
    """
    Generate content using an image.

    Request syntax
    ---------------------

    Response syntax (200)
    ---------------------
    {
        "Title": "",
        "Text": str
    }

    Response syntax (500)
    ---------------------
    {
        "Msg": a formatted traceback if an uncaught error was thrown
    }
    """
    pass


@blueprint.route("/file", methods=["POST"])
def file():
    """
    Generate content using a file.

    Request syntax
    ---------------------

    Response syntax (200)
    ---------------------
    {
        "Title": "",
        "Text": str
    }

    Response syntax (500)
    ---------------------
    {
        "Msg": a formatted traceback if an uncaught error was thrown
    }
    """
    pass


@blueprint.route("/sentences", methods=["POST"])
def sentences():
    """
    Generate sentences for a given word.
    """
    pass
