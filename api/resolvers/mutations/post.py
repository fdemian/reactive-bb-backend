from api.database.models import Post, PostEdits, User, Topic
from datetime import datetime
from sqlalchemy import select
from api.resolvers.auth import login_required, mod_required
from sqlalchemy.orm import Session
from api.engine import get_engine_from_context
from sqlalchemy.exc import SQLAlchemyError


def log_mod_operation(current_date, operation, mod_user):
    pass


@mod_required
def edit_post(_, info, post, user, content):
    current_date = datetime.now()
    db_engine = get_engine_from_context(info)
    with Session(db_engine) as session:
        try:
            post_to_edit = session.scalars(select(Post).filter_by(id=post)).first()

            # Log moderator edit for the record.
            post_edit = PostEdits(
                user_id=user,
                date=current_date,
                edited_post=post,
                previous_text=post_to_edit.content,
                current_text=content,
            )

            # Edit post
            post_to_edit.content = content
            post_to_edit.edited = True

            session.add(post_edit)
            session.add(post_to_edit)

            session.commit()

            return {"id": post_to_edit.id, "ok": True, "content": content}
        except SQLAlchemyError:
            session.rollback()
            return {"ok": False, "id": None, "content": None}


@mod_required
def delete_post(_, info, post, user):
    # Create new post.
    current_date = datetime.now()
    db_engine = get_engine_from_context(info)
    with Session(db_engine) as session:
        try:
            post_to_delete = session.scalars(select(Post).filter_by(id=post)).first()
            original_user = post_to_delete.user_id

            session.delete(post_to_delete)
            # db_session.add(post)
            session.commit()

            # Log post deletion.

            # Is the post being deleted by the original user or by a mod?
            if user is not original_user:
                mod_user = session.scalars(select(User).filter_by(id=user)).first()
                log_mod_operation(current_date, "POST_DELETION", mod_user)

            return {"ok": True, "id": post}
        except SQLAlchemyError:
            session.rollback()
            return {"ok": False, "id": None}


@login_required
def create_post(_, info, user, topic, content):
    # Create new post.
    current_date = datetime.now()
    post = Post(
        content=content,
        created=current_date,
        edited=False,
        user_id=user,
        topic_id=topic,
    )
    db_engine = get_engine_from_context(info)
    with Session(db_engine) as session:
        try:
            session.add(post)

            # Bump replies number.
            topic = session.scalars(select(Topic).filter_by(id=topic)).one()
            session.add(topic)
            session.commit()

            return {
                "id": post.id,
                "content": post.content,
                "user": {
                    "id": 0,
                    "avatar": topic.user.avatar,
                    "username": topic.user.username,
                },
            }
        except SQLAlchemyError:
            session.rollback()
            print("Error inserting post")
            print("User {0}".format(user.username))
            print("Content {0}".format("content"))
            print("Topic {0}".format(topic.name))

            return {
                "id": None,
                "content": "{}",
                "user": {"id": 0, "avatar": None, "username": None},
            }
