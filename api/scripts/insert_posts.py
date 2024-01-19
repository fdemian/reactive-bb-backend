from api.database.utils import get_engine
from api.database.models import Post
from os import path
from datetime import datetime

config_file = "../../config.json"
config_file_path = path.join(path.dirname(__file__), config_file)


def create_post(user_id, topic_id, number):
    current_date = datetime.now()
    post_text = (
        '{"blocks":[{"key":"2usen","text":"Post# '
        + str(number)
        + '","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}}],"entityMap":{}}'
    )
    post = Post()
    post.content = post_text
    post.user_id = user_id
    post.topic_id = topic_id
    post.created = current_date

    return post


def insert_all_posts():
    engine = get_engine(db_name)
    with Session(engine) as session:
        for n in range(500):
            user_id = 1
            topic_id = 2
            post = create_post(user_id, topic_id, n)
            #
            session.add(post)

        session.commit()
