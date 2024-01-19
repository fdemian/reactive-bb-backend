from api.database.models import Chat, User
from sqlalchemy import select, or_, and_
from sqlalchemy.orm import Session
from api.engine import get_engine_from_context


CHATS_PAGE_LIMIT = 5


def resolve_user_chats(_, info, user):
    db_engine = get_engine_from_context(info)
    with Session(db_engine) as session:
        users = (
            session.execute(
                select(User)
                .join(
                    Chat,
                    onclause=(
                        or_(Chat.author_id == User.id, Chat.recipient_id == User.id)
                    ),
                )
                .where(
                    and_(
                        User.id != user,
                        or_(Chat.author_id == user, Chat.recipient_id == user),
                    )
                )
                .limit(CHATS_PAGE_LIMIT)
                .offset(0)
                .group_by(User.id)
            )
            .scalars()
            .unique()
            .all()
        )
        return users


def resolve_chat(_, info, userA, userB, offset, limit):
    """
    TODO: rename this.
    UserA is the user requesting the chat.
    UserB is the user with whom the user was conversing with.
    """
    db_engine = get_engine_from_context(info)
    with Session(db_engine) as session:
        chats = session.scalars(
            select(Chat)
            .where(
                or_(
                    and_(Chat.author_id == userA, Chat.recipient_id == userB),
                    and_(Chat.author_id == userB, Chat.recipient_id == userA),
                )
            )
            .order_by(Chat.date)
            .limit(limit)
            .offset(offset)
        ).all()
        return chats
