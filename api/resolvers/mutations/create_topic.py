from api.database.models import Topic, Post
from datetime import datetime
from api.resolvers.auth import login_required, mod_required
from sqlalchemy.orm import Session
from api.engine import get_engine_from_context
from sqlalchemy import select


@login_required
async def increase_view_count(_, info, topic):
    db_engine = get_engine_from_context(info)
    with Session(db_engine) as session:
        try:
            topic = session.scalars(select(Topic).filter_by(id=topic)).one()
            topic.views = topic.views + 1
            session.add(topic)
            session.commit()
            return {"ok": True, "id": topic.id}
        except:
            return {"ok": False, "id": None}


@login_required
def create_topic(_, info, name, user, content, category, tags):
    db_engine = get_engine_from_context(info)
    with Session(db_engine) as session:
        # Add topic.
        current_date = datetime.now()
        topic = Topic(
            name=name,
            replies=1,
            views=0,
            closed=False,
            pinned=False,
            created=current_date,
            user_id=user,
            category_id=category,
            tags=tags,
        )
        session.add(topic)
        session.commit()

        # Create first post of the topic.
        post = Post(
            content=content,
            user_id=user,
            topic_id=topic.id,
            edited=False,
            created=current_date,
        )
        session.add(post)
        session.commit()

        return {"id": topic.id, "ok": True}


@mod_required
def close_topic(_, info, topic):
    db_engine = get_engine_from_context(info)
    with Session(db_engine) as session:
        topic = session.scalars(select(Topic).filter_by(id=topic)).one()
        topic.closed = True
        session.add(topic)
        session.commit()
        return True


@mod_required
def reopen_topic(_, info, topic):
    db_engine = get_engine_from_context(info)
    with Session(db_engine) as session:
        topic = session.scalars(select(Topic).filter_by(id=topic)).one()
        topic.closed = False
        session.add(topic)
        session.commit()
        return True


@mod_required
def delete_topic(_, info, topic):
    db_engine = get_engine_from_context(info)
    with Session(db_engine) as session:
        topic = session.scalars(select(Topic).filter_by(id=topic)).one()
        session.delete(topic)
        session.commit()
        return True


@mod_required
def pin_topic(_, info, topic):
    db_engine = get_engine_from_context(info)
    with Session(db_engine) as session:
        topic = session.scalars(select(Topic).filter_by(id=topic)).one()
        topic.pinned = not topic.pinned
        session.add(topic)
        session.commit()
        return True
