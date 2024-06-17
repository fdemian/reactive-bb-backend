from api.database.models import Topic
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from api.engine import get_engine_from_context

"""
import logging

async def log_request(info):
    logger = logging.getLogger("admin.graphql")
    body_b = await info.context['request'].body()
    logger.info(str(body_b.decode('UTF-8')))
"""

PINNED_TOPICS_LIMIT = 5


# Pinned topics do not count towards the page limit.
def get_pinned_topics(_, info):
    db_engine = get_engine_from_context(info)
    with Session(db_engine) as session:
        topics = session.scalars(
            select(Topic)
            .where(Topic.pinned is True)
            .order_by(Topic.created.desc())
            .limit(PINNED_TOPICS_LIMIT)
        ).all()
        return topics


def resolve_topics(_, info, offset, limit):
    # await log_request(info)
    db_engine = get_engine_from_context(info)
    with Session(db_engine) as session:
        topics = session.scalars(
            select(Topic)
            .where(Topic.pinned == False)
            .order_by(Topic.created.desc())
            .limit(limit)
            .offset(offset)
        ).all()
        topics_count = session.scalar(select(func.count(Topic.id)))
        return {"topics": topics, "topicsCount": topics_count}


def resolve_topic(_, info, topic_id):
    db_engine = get_engine_from_context(info)
    with Session(db_engine) as session:
        topic = session.scalars(select(Topic).filter_by(id=topic_id)).first()
        return topic


def resolve_topics_by_user(_, info, user_id):
    db_engine = get_engine_from_context(info)
    with Session(db_engine) as session:
        topics = session.scalars(
            select(Topic).filter_by(user_id=user_id).order_by(Topic.created.desc())
        ).all()
        return topics
