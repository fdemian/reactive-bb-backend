from api.database.models import Bookmark
from api.resolvers.auth import login_required
from sqlalchemy.orm import Session
from api.engine import get_engine_from_context
from sqlalchemy import select


@login_required
def bookmark_post(_, info, post, user):
    db_engine = get_engine_from_context(info)
    with Session(db_engine) as session:
        try:
            bookmark = Bookmark(user_id=user, post_id=post)
            session.add(bookmark)
            session.commit()

            return {"id": bookmark.id, "ok": True, "postId": post, "userId": user}
        except:
            return {"id": 0, "ok": False, "postId": post, "userId": user}


@login_required
def remove_bookmark(_, info, post, user):
    db_engine = get_engine_from_context(info)
    with Session(db_engine) as session:
        bookmark = session.scalars(
            select(Bookmark).filter_by(user_id=user, post_id=post)
        ).one()
        id = bookmark.id
        session.delete(bookmark)
        session.commit()

        return {"id": id, "ok": True, "postId": post, "userId": user}
