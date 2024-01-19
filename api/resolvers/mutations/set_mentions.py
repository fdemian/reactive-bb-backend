import json
from api.resolvers.save_notification import save_notification
from api.database.models import User
from api.resolvers.auth import login_required
from sqlalchemy import select
from sqlalchemy.orm import Session
from api.utils.utils import get_app_state_from_context


@login_required
async def set_mentions(_, info, link, user, mentioned):
    app_state = get_app_state_from_context(info)
    broadcast = app_state.broadcast
    db_engine = app_state.engine
    with Session(db_engine) as session:
        originator = session.scalars(select(User).filter_by(username=user)).one()
        users = session.scalars(select(User).filter(User.username.in_(mentioned))).all()

        for mentionedUser in users:
            notification = {
                "id": 0,
                "user": {
                    "id": mentionedUser.id,
                    "username": mentionedUser.username,
                    "avatar": mentionedUser.avatar,
                },
                "originator": {
                    "id": originator.id,
                    "username": originator.username,
                    "avatar": originator.avatar,
                },
                "link": link,
                "type": "mention",
                "read": False,
            }
            await broadcast.publish(
                channel="notificationAdded", message=json.dumps(notification)
            )
            save_notification(notification, session)
