from api.database.models import FlaggedPost
from api.resolvers.auth import login_required
from sqlalchemy import select
from sqlalchemy.orm import Session
from api.engine import get_engine_from_context


@login_required
def flag_post(_, info, post, user, reason, text):
    flagged_post = FlaggedPost(
        post_id=post, user_id=user, reason_id=reason, reason_text=text
    )
    db_engine = get_engine_from_context(info)
    with Session(db_engine) as session:
        session.add(flagged_post)
        session.commit()
    return True


@login_required
def remove_flag(_, info, post, user):
    db_engine = get_engine_from_context(info)
    with Session(db_engine) as session:
        to_remove = session.scalars(
            select(FlaggedPost).filter_by(post_id=post, user_id=user)
        ).one()
        session.delete(to_remove)
        session.commit()
        return {"ok": True, "postId": post, "userId": user}
