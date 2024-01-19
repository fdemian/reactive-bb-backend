from sqlalchemy.engine import Engine


def get_engine_from_context(info) -> Engine:
    return info.context["request"].app.state.engine


def get_engine_from_request(request) -> Engine:
    return request.app.state.engine
