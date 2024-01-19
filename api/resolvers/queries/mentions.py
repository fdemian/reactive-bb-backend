from api.database.models import User
from sqlalchemy import select
from sqlalchemy.orm import Session
from api.engine import get_engine_from_context


MENTION_CANDIDATES_LIMIT = 5


def resolve_mention_candidates(_, info, search):
    db_engine = get_engine_from_context(info)
    with Session(db_engine) as session:
        users = session.scalars(
            select(User)
            .where(User.username.ilike("%" + search + "%"))
            .limit(MENTION_CANDIDATES_LIMIT)
        ).all()
        if not users:
            return []  # TODO: raise Exception('Requested user does not exist.')
        else:
            return users
