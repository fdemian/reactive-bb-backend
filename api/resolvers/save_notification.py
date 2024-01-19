from api.database.models import Notification


def save_notification(notification_to_save, session):
    notification = Notification()
    notification.link = notification_to_save["link"]
    notification.type = notification_to_save["type"]
    notification.read = notification_to_save["read"]
    notification.originator_id = int(notification_to_save["originator"]["id"])
    notification.user_id = int(notification_to_save["user"]["id"])
    session.add(notification)
    session.commit()

    return notification.id
