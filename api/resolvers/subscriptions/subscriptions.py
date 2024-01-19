from ariadne import SubscriptionType
from .mention import notification_generator, notification_resolver
from .chats import (
    chat_generator,
    chat_resolver,
    chat_notification_resolver,
    chat_notification_generator,
)

# Subscriptions.
subscriptions = SubscriptionType()

subscriptions.set_field("notificationAdded", notification_resolver)
subscriptions.set_source("notificationAdded", notification_generator)

subscriptions.set_field("chatAdded", chat_resolver)
subscriptions.set_source("chatAdded", chat_generator)

subscriptions.set_field("chatNotification", chat_notification_resolver)
subscriptions.set_source("chatNotification", chat_notification_generator)
