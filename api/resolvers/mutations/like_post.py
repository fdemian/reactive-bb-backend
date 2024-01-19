import json
import sys
from api.resolvers.save_notification import save_notification
from api.database.models import Like, User
from api.resolvers.auth import login_required
from sqlalchemy import select
from sqlalchemy.orm import Session
from api.utils.utils import get_app_state_from_context


@login_required
async def like_post(_, info, post, topic, user, originator):
    app_state = get_app_state_from_context(info)
    broadcast = app_state.broadcast
    db_engine = app_state.engine
    with Session(db_engine) as session:
        try:
            like = Like(user_id=user, post_id=post)
            originator_obj = session.scalars(
                select(User).filter_by(id=originator)
            ).one()
            user_obj = session.scalars(select(User).filter_by(id=user)).one()
            notification = {
                "id": 0,
                "link": f"/postlink/{str(post)}",
                "type": "like",
                "originator": {
                    "id": originator_obj.id,
                    "username": originator_obj.username,
                    "avatar": originator_obj.avatar,
                },
                "user": {
                    "id": user_obj.id,
                    "username": user_obj.username,
                    "avatar": user_obj.avatar,
                },
                "read": False,
            }
            not_id = save_notification(notification, session)
            session.add(like)
            session.commit()
            notification["id"] = not_id
            await broadcast.publish(
                channel="notificationAdded", message=json.dumps(notification)
            )
            return {"id": like.id, "ok": True, "postId": post, "likes": 0}
        except:
            print(f"Unknown Error - {sys.exc_info()[1]}")
            print(f"Details - {sys.exc_info()}")
            return {"id": 0, "ok": False, "postId": post, "likes": 0}


@login_required
def remove_like(_, info, post, user):
    app_state = get_app_state_from_context(info)
    db_engine = app_state.engine

    with Session(db_engine) as session:
        like = session.query(Like).filter_by(post_id=post, user_id=user).one()

        id = like.id
        session.delete(like)
        session.commit()

        return {"id": id, "ok": True, "postId": post, "userId": user, "likes": 0}
