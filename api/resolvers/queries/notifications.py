from api.database.models import Notification
from sqlalchemy import select
from sqlalchemy.orm import Session
from api.engine import get_engine_from_context

NOTIFICATION_CANDIDATES_LIMIT = 5


def resolve_notifications(_, info, user):
    db_engine = get_engine_from_context(info)
    with Session(db_engine) as session:
        notifications = session.scalars(
            select(Notification)
            .filter_by(user_id=user, read=False)
            .limit(NOTIFICATION_CANDIDATES_LIMIT)
        ).all()
        return notifications


def resolve_all_notifications(_, info, user, limit, offset):
    db_engine = get_engine_from_context(info)
    with Session(db_engine) as session:
        notifications = session.scalars(
            select(Notification).filter_by(user_id=user).limit(limit).offset(offset)
        ).all()
        return notifications
