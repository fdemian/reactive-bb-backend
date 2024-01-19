import re
from ariadne.asgi import GraphQL
from ariadne.asgi.handlers import GraphQLTransportWSHandler
from graphql.error import GraphQLError, GraphQLFormattedError


def hide_field_suggestion_fmt(
    error: GraphQLError, debug: bool = False
) -> GraphQLFormattedError:
    formatted = error.formatted
    formatted["message"] = re.sub(r"Did you mean.*", "", formatted["message"])
    return formatted


def get_graphql_handler(graphl_schema, environment):
    if environment == "development":
        graphql_handler = GraphQL(
            schema=graphl_schema,
            debug=True,
            introspection=True,
            websocket_handler=GraphQLTransportWSHandler(),
            logger="admin.graphql",
        )
    else:
        graphql_handler = GraphQL(
            schema=graphl_schema,
            debug=False,
            introspection=False,
            websocket_handler=GraphQLTransportWSHandler(),
            error_formatter=hide_field_suggestion_fmt,
            logger="admin.graphql",
        )
    return graphql_handler
