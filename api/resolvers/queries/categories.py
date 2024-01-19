from api.database.models import Category, Topic
from sqlalchemy import select
from sqlalchemy.orm import Session
from api.engine import get_engine_from_context


def resolve_categories(_, info):
    db_engine = get_engine_from_context(info)
    with Session(db_engine) as session:
        categories = session.scalars(select(Category)).all()
        return categories


def resolve_category(_, info, id):
    db_engine = get_engine_from_context(info)
    with Session(db_engine) as session:
        if id == -1:
            topics = session.scalars(select(Topic).filter_by(category_id=None)).all()
            return {
                "id": 0,
                "name": "Uncategorized",
                "description": "",
                "topics": topics,
            }
        category = session.query(Category).filter_by(id=id).one()
        return category
