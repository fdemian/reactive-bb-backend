from api.scripts.insertdata.insert_posts import insert_all_posts
from api.database.models import Topic
from datetime import datetime


def generate_topic(name, user_id, category_id, posts):
    current_date = datetime.now()
    topic = {
        "name": name,
        "views": 0,
        "closed": False,
        "created": current_date,
        "pinned": False,
        "userId": user_id,
        "tags": "",
        "categoryId": category_id,
        "posts": posts,
    }
    return topic


def insert_topic(session, topic_to_insert):
    topic = Topic()
    topic.name = topic_to_insert["name"]
    topic.views = topic_to_insert["views"]
    topic.closed = topic_to_insert["closed"]
    topic.created = topic_to_insert["created"]
    topic.pinned = topic_to_insert["pinned"]
    topic.user_id = topic_to_insert["userId"]
    topic.category_id = topic_to_insert["categoryId"]
    topic.tags = topic_to_insert["tags"]

    session.add(topic)
    session.commit()
    insert_all_posts(session, topic, topic_to_insert["posts"])
    return topic.id
