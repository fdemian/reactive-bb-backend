import logging
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql import func, column
from api.database.models import Topic, Post
from api.resolvers.auth import login_required
from sqlalchemy.orm import Session
from sqlalchemy import select
from api.engine import get_engine_from_context


def map_topic(topic):
    return {
        "id": topic.posts[0].id,
        "text": topic.posts[0].content,
        "topicId": topic.id,
        "topic": topic.name,
    }


def map_post(post):
    return {
        "id": post.id,
        "text": post.content,
        "topicId": post.topic.id,
        "topic": post.topic.name,
    }


def unique_results(search_list):
    return list({v["id"]: v for v in search_list}.values())


@login_required
def resolve_search(_, info, term, where, offset, limit):
    search_results = []
    topic_results = []
    posts_results = []
    total_results_count = 0

    db_engine = get_engine_from_context(info)
    with Session(db_engine) as session:
        try:
            if "titles" in where:
                topics_from_db = session.scalars(
                    select(Topic)
                    .where(column("topics.name", is_literal=True).match(term))
                    .limit(limit)
                    .offset(offset)
                ).all()

                topics_count = session.scalar(
                    func.count(func.to_tsvector(Topic.name).match(term))
                )

                total_results_count = total_results_count + topics_count
                topic_results = list(map(map_topic, topics_from_db))
                search_results = topic_results

            if "posts" in where:
                posts_from_db = session.scalars(
                    select(Post)
                    .where(func.to_tsvector(func.json(Post.content)).match(term))
                    .limit(limit)
                    .offset(offset)
                ).all()

                posts_count = session.scalar(
                    func.count(func.to_tsvector(func.json(Post.content)).match(term))
                )
                posts_results = list(map(map_post, posts_from_db))
                search_results = posts_results
                total_results_count = total_results_count + posts_count

            if "titles" in where and "posts" in where:
                search_results = unique_results(topic_results + posts_results)
                search_results = search_results

            return {"results": search_results, "total": total_results_count}

        except NoResultFound:
            whereStr = "["
            if "posts" in where:
                whereStr = whereStr + "posts"

            if "titles" in where:
                whereStr = whereStr + "titles"
            whereStr = "]"
            logging.error(f"Search results not found. TERM={term}, WHERE={whereStr}")
            return []
