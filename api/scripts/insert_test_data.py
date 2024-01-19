from sqlalchemy.orm import Session
from api.database.utils import get_engine
from api.scripts.insertdata.insert_user import (
    insert_test_user,
    user,
    user2,
    mod_user,
    admin_user,
    banned_user,
)
from api.scripts.insertdata.insert_category import insert_test_category, category
from api.scripts.insertdata.insert_topics import insert_topic, generate_topic
from api.scripts.insertdata.insert_posts import generate_numbered_posts
from api.read_config import config_to_environ_sync


def insert_actual_data(session):
    user_id = insert_test_user(session, user)
    insert_test_user(session, user2)
    insert_test_user(session, mod_user)
    insert_test_user(session, admin_user)
    insert_test_user(session, banned_user)
    category_id = insert_test_category(
        session, category["name"], category["description"]
    )
    numbered_posts = generate_numbered_posts(1000)
    posts = [{"text": p, "user": user_id} for p in numbered_posts]
    topic = generate_topic("T-1000", user_id, category_id, posts)
    insert_topic(session, topic)
    return user_id


def insert_test_data():
    config_to_environ_sync()
    from api.engine import db_engine

    with Session(db_engine) as session:
        return insert_actual_data(session)


def insert_test_data_db():
    engine = get_engine()
    with Session(engine) as session:
        return insert_actual_data(session)


def main():
    insert_test_data()
