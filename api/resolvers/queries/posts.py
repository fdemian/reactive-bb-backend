from sqlalchemy import select
from api.database.models import Post, Topic
from ariadne.exceptions import HttpError
from math import ceil
from sqlalchemy import text
from sqlalchemy.orm import Session
from api.engine import get_engine_from_context


def resolve_posts(_, info, topicId, offset, limit):
    db_engine = get_engine_from_context(info)
    with Session(db_engine) as session:
        posts = session.scalars(
            select(Post)
            .filter_by(topic_id=topicId)
            .order_by(Post.id)
            .limit(limit)
            .offset(offset)
        ).all()
        return posts


def resolve_posts_by_user(_, info, id):
    db_engine = get_engine_from_context(info)
    with Session(db_engine) as session:
        posts = session.scalars(
            select(Post).filter_by(user_id=id).order_by(Post.created.desc())
        ).all()
        return posts


def resolve_post_link(_, info, post, itemscount):
    """
    Using the topic's id, post id and items per page we are able to deduce
    the position of a given post in a thread's page.
    """
    db_engine = get_engine_from_context(info)
    with Session(db_engine) as session:
        try:
            post_info = session.scalars(select(Post).filter_by(id=post)).first()
            topic = post_info.topic_id

            SELECT_SQL = """
                 SELECT  Sequence_no FROM  (
                 SELECT  ROW_NUMBER() OVER (ORDER BY id, user_id, topic_id)  Sequence_no, id
                 FROM  posts WHERE topic_id = {} ORDER BY created
                 ) AS P WHERE P.id = {};
                """.format(topic, post)

            result = session.execute(text(SELECT_SQL))
            res_as_array = [row[0] for row in result]
            location = res_as_array[0]
            page_number = ceil(location / itemscount)

            topic_obj = session.scalars(select(Topic).filter_by(id=topic)).one()
            return {"topicId": topic, "page": page_number, "name": topic_obj.name}
        except:
            raise HttpError("404")
