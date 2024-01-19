from api.database.models import User  # , UserActivation
from sqlalchemy import select
from sqlalchemy.orm import Session
from api.engine import get_engine_from_context


def resolve_user_availability(_, info, username):
    db_engine = get_engine_from_context(info)
    with Session(db_engine) as session:
        user_query = session.execute(
            select(User).filter_by(username=username)
        ).scalar_one_or_none()
        if user_query is not None:
            return {"exists": True, "message": "Username taken."}
        else:
            return {"exists": False, "message": "Username available."}
