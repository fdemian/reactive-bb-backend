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