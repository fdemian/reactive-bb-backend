import json
from api.utils.utils import get_app_state_from_context
import datetime

DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


async def chat_generator(_, info, **kwargs):
    user_a = kwargs.get("userA")
    user_b = kwargs.get("userB")
    app_state = get_app_state_from_context(info)
    broadcast = app_state.broadcast
    async with broadcast.subscribe(channel="chatAdded") as subscriber:
        async for event in subscriber:
            json_message = json.loads(event.message)
            if (
                json_message["author"]["id"] == user_a
                and json_message["recipient"]["id"] == user_b
            ) or (
                json_message["author"]["id"] == user_b
                and json_message["recipient"]["id"] == user_a
            ):
                json_message["date"] = datetime.datetime.strptime(
                    json_message["date"], DATE_FORMAT
                )
                yield json_message
            else:
                yield {}


def chat_resolver(chat, info, **kwargs):
    return chat


async def chat_notification_generator(_, info, **kwargs):
    user = kwargs.get("user")
    app_state = get_app_state_from_context(info)
    broadcast = app_state.broadcast
    async with broadcast.subscribe(channel="chatNotification") as subscriber:
        async for event in subscriber:
            json_message = json.loads(event.message)
            if (
                json_message["author"]["id"] == user
                or json_message["recipient"]["id"] == user
            ):
                json_message["date"] = datetime.datetime.strptime(
                    json_message["date"], DATE_FORMAT
                )
                yield json_message
            else:
                yield {}


def chat_notification_resolver(chat, info, **kwargs):
    return chat
