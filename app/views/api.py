from flask import Blueprint, make_response, request, jsonify

from app.json_schemas import API, validate_schema
from app.schema import schema
from app.utils.dictionary.infer import get_inference
from app.utils.logging import logger

blueprint = Blueprint("api", __name__)


@blueprint.route("/graphql", methods=["GET", "POST"])
def graphql():
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
    try:
        query = validated_data["Query"]
        try:
            context = validated_data["Context"]
        except KeyError:
            context = None

        inference = get_inference(query, context=context)
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
                    ]  # TODO: enable user filtering
                } for sense in entry["senses"]]
            })

    except Exception as e:
        logger.exception(e)
        return make_response({"Message": "An unexpected error occured."}, 500)

    return make_response({"Message": "Success.", "Result": result}, 200)
