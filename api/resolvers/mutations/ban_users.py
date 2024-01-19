from api.resolvers.auth import mod_required
from api.resolvers.queries.user import get_user_if_exists
from sqlalchemy.orm import Session
from api.engine import get_engine_from_context


@mod_required
def ban_user(_, info, user, expires, reason):
    db_engine = get_engine_from_context(info)
    with Session(db_engine) as session:
        try:
            user_to_ban = get_user_if_exists(session, user)

            if user_to_ban is None:
                return False

            user_to_ban.banned = True
            user_to_ban.ban_reason = reason
            user_to_ban.ban_expires = expires
            session.add(user_to_ban)
            session.commit()

            return True
        except:
            return False


@mod_required
def remove_user_ban(_, info, user):
    db_engine = get_engine_from_context(info)
    with Session(db_engine) as session:
        try:
            user_to_unban = get_user_if_exists(session, user)

            if user_to_unban is None:
                return False

            user_to_unban.banned = False
            user_to_unban.ban_reason = None
            user_to_unban.expires = None
            session.add(user_to_unban)
            session.commit()

            return True
        except:
            return False
