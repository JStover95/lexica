from flask import Blueprint, make_response, request, jsonify

from app.json_schemas import API, validate_schema
from app.schema import schema
from app.utils.dictionary.infer import get_inference
from app.utils.logging import logger

blueprint = Blueprint("api", __name__)


@blueprint.route("/graphql", methods=["POST"])
def graphql():
    """
    Handle GraphQL requests via POST method.

    This endpoint processes incoming GraphQL queries by extracting the query,
    variables, and operation name from the request. It then executes the GraphQL
    query using the predefined schema and returns the result in JSON format.

    Request Body (JSON):
        - query (str): The GraphQL query string.
        - variables (dict, optional): A dictionary of variables for
            parameterized queries.
        - operationName (str, optional): The name of the operation to execute
            (useful for queries with multiple operations).

    Returns:
        Response: A JSON response containing the query execution result.
                  The response includes the following keys:
                  - data (dict): The result data from the GraphQL query
                    execution.
                  - errors (list, optional): A list of error messages if any
                    errors occurred during query execution.

    Example Request (POST):
        {
            "query": "query { user(id: 1) { email } }",
            "variables": {"id": 1},
            "operationName": "getUser"
        }

    Example Response:
        {
            "data": {
                "user": {
                    "email": "john.doe@example.com"
                }
            },
            "errors": [
                "Some error message"
            ]
        }

    HTTP Status:
        - 200 OK: The request was successfully processed and a valid response
                  was returned.
    """
    data = request.get_json()

    # Extract the query, variables, and operation name from the request
    query = data.get("query")
    variables = data.get("variables")
    operation_name = data.get("operationName")

    # Execute the GraphQL query
    result = schema.execute(
        query,
        variables=variables,
        operation_name=operation_name,
    )

    # Format the execution result and send the response
    response_data = {
        "data": result.data
    }

    if result.errors:
        response_data["errors"] = [str(e) for e in result.errors]

    response = jsonify(response_data)
    response.status_code = 200
    return response


@blueprint.route("/infer", methods=["POST"])
@validate_schema(API.infer_schema)
def infer(validated_data: API.InferRequestType):
    """
    Process a POST request to infer the most appropriate dictionary definitions
    for a set of words.

    This endpoint takes a JSON payload containing a list of words ("Query") and
    an optional "Context" string (e.g., a sentence or paragraph that contains
    the words in "Query"). The endpoint then queries a dictionary to retrieve 
    definitions for each word. The definitions are ranked based on their
    relevance to the provided context, where a rank of 0 indicates that the
    definition is not relevant to the context and a rank of 1 indicates that it
    is the most appropriate definition.

    The endpoint returns list containing one dictionary entry for each word in
    "Query", where each entry includes the word's written form, part of speech,
    and a list of senses (definitions) with their respective ranks.
    Additionally, each sense includes a list of equivalents (translations) in
    English.

    Request Body (JSON):
        - Query (list of str): A list of words for which to retrieve
            dictionary definitions.
        - Context (str, optional): A string that provides context for ranking
            the definitions (e.g., a sentence or paragraph).

    Response (JSON):
        - Message (str): A status message indicating success or failure.
        - Result (list): A list of dictionary entries for each word in "Query".
            Each entry contains:
            - writtenForm (str): The word's written form.
            - partOfSpeech (str): The part of speech for the word.
            - senses (list): A list of senses (definitions) for the word. Each
                sense includes:
                - definition (str): The definition of the sense.
                - rank (float): The relevance score of the definition to the
                    provided context (0 to 1).
                - equivalents (list): A list of equivalent translations.
                    Currently this only returns one equivalent in English. Each
                    equivalent includes:
                    - equivalentLanguage (str): The language of the equivalent
                        (e.g., "영어" for English).
                    - equivalent (str): The equivalent translation of the word.
                    - definition (str): The definition of the equivalent
                        translation.

    Raises:
        - 500 Internal Server Error: If an unexpected error occurs during the
            inference process.

    Returns:
        - 200 OK: If the request is successfully processed.
        - 500 Internal Server Error: If an unexpected error occurs.
    """
    try:
        query = validated_data["Query"]
        try:
            context = validated_data["Context"]
        except KeyError:
            context = None

        # Execute the query
        inference = get_inference(query, context=context)

        # Transform the query results into the correct response format
        result = []
        for entry in inference:
            result.append({
                "writtenForm": entry["writtenForm"],
                "partOfSpeech": entry["partOfSpeech"],
                "senses": [{
                    "definition": sense["definition"],
                    "rank": sense["rank"],
                    "equivalents": [
                        {
                            "equivalentLanguage": equivalent["equivalentLanguage"],
                            "equivalent": equivalent["equivalent"],
                            "definition": equivalent["definition"],
                        }
                        for equivalent in sense["equivalents"]
                        if equivalent["equivalentLanguage"] == "영어"
                    ]  # TODO: Enable user filtering by language
                } for sense in entry["senses"]]
            })

    except Exception as e:
        logger.exception(e)
        return make_response({"Message": "An unexpected error occured."}, 500)

    return make_response({"Message": "Success.", "Result": result}, 200)
