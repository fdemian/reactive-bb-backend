from api.database.models import Bookmark
from sqlalchemy import select, column
from sqlalchemy.orm import Session
from api.engine import get_engine_from_context


def resolve_bookmarks_by_user(_, info, user):
    db_engine = get_engine_from_context(info)
    with Session(db_engine) as session:
        bookmarks = session.scalars(select(Bookmark).filter_by(user_id=user)).all()
        return bookmarks


def resolve_bookmarks_by_post_list(_, info, user, posts):
    db_engine = get_engine_from_context(info)
    with Session(db_engine) as session:
        bookmarks = session.scalars(
            select(Bookmark).filter_by(user_id=user).where(column("post_id").in_(posts))
        ).all()
        return bookmarks
