from flask import Blueprint, request, jsonify
from l2ai.schema import schema

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
    print(result)

    # Format the execution result and send the response
    response_data = {
        "data": result.data
    }

    if result.errors:
        response_data["errors"] = [str(e) for e in result.errors]

    response = jsonify(response_data)
    response.status_code = 200
    return response
