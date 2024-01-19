import json
from datetime import datetime, date
from api.database.models import Chat
from api.resolvers.auth import login_required
from sqlalchemy.orm import Session
from api.utils.utils import get_app_state_from_context


DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


class DateTimeEncoder(json.JSONEncoder):
    # Override the default method
    def default(self, obj):
        if isinstance(obj, (date, datetime)):
            return obj.strftime(DATE_FORMAT)

        return json.JSONEncoder.default(self, obj)


@login_required
async def send_message(_, info, author, recipient, message, newchat):
    current_date = datetime.now()
    chat = Chat(
        author_id=author, recipient_id=recipient, content=message, date=current_date
    )

    app_state = get_app_state_from_context(info)
    broadcast = app_state.broadcast
    db_engine = app_state.engine
    with Session(db_engine) as session:
        session.add(chat)
        session.commit()

        new_chat = {
            "date": chat.date,
            "content": chat.content,
            "author": {
                "id": chat.author.id,
                "avatar": chat.author.avatar,
                "username": chat.author.username,
            },
            "recipient": {
                "id": chat.recipient.id,
                "avatar": chat.recipient.avatar,
                "username": chat.recipient.username,
            },
        }
        await broadcast.publish(
            channel="chatAdded", message=json.dumps(new_chat, cls=DateTimeEncoder)
        )

        # If the message that was added is the first message on the conversation, notify the user.
        if newchat:
            chat_notification = {
                "read": False,
                "author": {
                    "id": chat.author.id,
                    "avatar": chat.author.avatar,
                    "username": chat.author.username,
                },
                "recipient": {
                    "id": chat.recipient.id,
                    "avatar": chat.recipient.avatar,
                    "username": chat.recipient.username,
                },
            }
            await broadcast.publish(
                channel="chatNotification", message=json.dumps(chat_notification)
            )

        return True
