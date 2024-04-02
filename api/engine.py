from sqlalchemy.engine import Engine


def get_engine_from_context(info) -> Engine:
    info_type = str(type(info))
    if info_type == "<class 'graphql.type.definition.GraphQLResolveInfo'>":
        return info.context["request"].app.state.engine
    else:
        if info_type == "<class 'starlette.requests.Request'>":
            return info.app.state.engine
        else:
            return info.context["request"].app.state.engine



def get_engine_from_request(request) -> Engine:
    return request.app.state.engine
