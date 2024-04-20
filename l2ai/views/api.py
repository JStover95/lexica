import logging
from l2ai.extensions import socketio

logger = logging.getLogger(__name__)


@socketio.event
def create_content():
    """
    Commit generated content to the database.

    Request Syntax
    --------------
    {
        "Title": str,
        "Text": str,
        "Method": str
    }
    """
    pass


@socketio.event
def get_content():
    """
    Get all of a user's content.

    Options
    -------
    id: str, the user id

    Response Syntax (200)
    ---------------------
    [
        {
            "ID": str,
            "Timestamp": int,
            "Title": str,
            "Text": str,
            "Method": str
        }
    ]
    """
    pass


@socketio.event
def update_content():
    """
    Update content.

    Request syntax
    ---------------------
    {
        "ID": str,
        "Title": str,
        "Text": str
    }

    Response syntax (200)
    ---------------------
    {
        "ID": str,
        "Timestamp": int,
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
def get_definitions():
    """
    Get the definitions of one or more words.

    Options
    -------
    id: str, the user id
    q: str, the query
    c: str, the content (i.e., the sentence containing the query)

    Response Syntax
    ---------------
    [
        {
            "Word": str,
            "Definitions": [
                {
                    "Score": float,
                    "Definition": str,
                    "UserScore": str
                },
                ...
            ]
        },
        ...
    ]
    """
    pass


@socketio.event
def update_user_score():
    """
    Update the user score of a certain word or definition.

    Options
    -------
    id: str, the user id
    defs: [str], a list of sense ids
    score: str
    """
    pass
