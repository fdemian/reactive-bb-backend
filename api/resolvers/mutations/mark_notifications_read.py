from sqlalchemy import update
from api.database.models import Notification
from sqlalchemy.orm import Session
from api.engine import get_engine_from_context
from api.resolvers.auth import login_required


@login_required
def mark_notifications_read(_, info, notifications):
    db_engine = get_engine_from_context(info)
    with Session(db_engine) as session:
        smt = (
            update(Notification)
            .where(Notification.id.in_(notifications))
            .values(read=True)
        )
        session.execute(smt)
        session.commit()
    return notifications
