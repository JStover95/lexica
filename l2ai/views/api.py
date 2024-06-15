import logging
from l2ai.extensions import socketio
from l2ai.utils.logging import logger


@socketio.event
def create_content(title: str, text: str, method: str):
    """
    Commit content to the database.

    Args:
        title (str): The content's title
        text (str): The content's text
        method (str): The content's creation method (i.e., paste, generate,
            image, file)

    Returns:
        str: The content's ObjectId
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
def delete_content():
    """
    Request Syntax
    --------------
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


@socketio.event
def create_explanation():
    """
    Request Syntax
    --------------
    {
        "Expression": str,
        "Definitions": [str],
        "Description": str,
        "ContentID": str,
        "ContentPosition": str
    }

    Response Syntax (500)
    ---------------------
    {
        "ID": str
    }
    """
    pass


@socketio.event
def get_explanations():
    """
    Request Syntax
    --------------
    {
        "ContentID": str
    }

    Response Syntax
    ---------------
    {
        "ID": str,
        "Expression": str,
        "Definitions": [str],
        "Description": str
    }
    """
    pass


@socketio.event
def update_explanation():
    """
    Request Syntax
    --------------
    {
        "ID": str,
        "Expression": str,
        "Definitions": [str],
        "Description": str
    }

    Response Syntax (500)
    ---------------------
    {
        "ID": str
    }
    """
