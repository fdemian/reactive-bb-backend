from sqlalchemy import select
from api.database.models import FlaggedPost
from sqlalchemy.orm import Session
from api.engine import get_engine_from_context


def resolve_flagged_posts(_, info, limit, offset):
    db_engine = get_engine_from_context(info)
    with Session(db_engine) as session:
        flagged_posts = session.scalars(
            select(FlaggedPost)
            .order_by(FlaggedPost.post_id)
            .limit(limit)
            .offset(offset)
        ).all()
        return flagged_posts
