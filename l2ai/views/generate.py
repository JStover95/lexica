import logging
from l2ai.extensions import socketio

logger = logging.getLogger(__name__)


@socketio.event
def generate_prompt():
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


@socketio.event
def generate_image():
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


@socketio.event
def generate_file():
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


@socketio.event
def generate_sentences():
    """
    Generate sentences for a given word.
    """
    pass
