from api.database.models import Post
from datetime import datetime


def generate_numbered_posts(count):
    posts = []
    for number in range(count):
        post_text = (
            '{"root":{"children":[{"children":[{"detail":0,"format":0,"mode":"normal","style":"","text":"Post#'
            + str(number)
            + '","type":"text","version":1}],"direction":"ltr","format":"","indent":0,"type":"paragraph",'
              '"version":1}],"direction":"ltr","format":"","indent":0,"type":"root","version":1}}'
        )
        posts.append(post_text)

    return posts


def create_post(user_id, topic_id, text):
    current_date = datetime.now()
    post = Post()
    post.content = text
    post.user_id = user_id
    post.topic_id = topic_id
    post.edited = False
    post.created = current_date

    return post


def insert_post(session, topic, post_to_insert):
    post = create_post(
        post_to_insert["userId"], post_to_insert["topicId"], post_to_insert["content"]
    )
    session.add(post)
    session.commit()


def insert_all_posts(session, topic, posts_to_insert):
    for _post in posts_to_insert:
        post = create_post(_post["user"], topic.id, _post["text"])
        session.add(post)
    session.commit()
