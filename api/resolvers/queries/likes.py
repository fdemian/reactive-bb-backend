from api.database.models import Like
from sqlalchemy import select
from sqlalchemy.orm import Session
from api.engine import get_engine_from_context


def get_likes_by_user(_, info, id):
    db_engine = get_engine_from_context(info)
    with Session(db_engine) as session:
        post_likes = session.execute(select(Like).filter_by(user_id=id)).scalars().all()
        return post_likes
