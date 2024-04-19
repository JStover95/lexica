import logging
from flask import Blueprint

blueprint = Blueprint("api", __name__)
logger = logging.getLogger(__name__)


blueprint.route("/create-content", methods=["POST"])
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


blueprint.route("/get-content")
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


blueprint.route("/update-content", methods=["POST"])
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
        "Text": str,
        "SurfaceMap": {
            "Units": [str, ...],
            "Ix": [
                [int, int],
                ...
            ]
        }
    }

    Response syntax (500)
    ---------------------
    {
        "Msg": a formatted traceback if an uncaught error was thrown
    }
    """
    pass


blueprint.route("/get-definitions")
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
                    "UserScore": str,
                    "Examples": [
                        {
                            "ko_KR": ...,
                            "en_US": ...
                        },
                        ...
                    ]
                },
                ...
            ]
        },
        ...
    ]
    """
    pass


@blueprint.route("/update-user-score")
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
