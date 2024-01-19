import json
from api.utils.utils import get_app_state_from_context


async def notification_generator(_, info, **kwargs):
    user = kwargs.get("user")
    app_state = get_app_state_from_context(info)
    broadcast = app_state.broadcast
    async with broadcast.subscribe(channel="notificationAdded") as subscriber:
        async for event in subscriber:
            json_message = json.loads(event.message)
            if json_message["user"]["id"] == user:
                yield json_message


def notification_resolver(message, info, user):
    return message
