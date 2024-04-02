from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from api.database.models import User
from sqlalchemy.orm import Session
from api.engine import get_engine_from_context
from sqlalchemy import select


def resolve_user(_, request, id):
    db_engine = get_engine_from_context(request)
    with Session(db_engine) as session:
        user = get_user_if_exists(session, id)
        if not user:
            raise Exception("Requested user does not exist.")
        else:
            return user


def get_user_if_exists(session, id):
    try:
        user = session.scalars(select(User).filter_by(id=id)).one()
        return user
    except MultipleResultsFound:
        return None
    except NoResultFound:
        return None


def user_to_dict(user):
    user_link = "/users/" + str(user.id) + "/" + user.username

    payload = {
        "id": user.id,
        "avatar": user.avatar,
        "username": user.username,
        "fullname": user.fullname,
        "email": user.email,
        "link": user_link,
        "about": user.about,
        "status": user.status,
        "banned": user.banned,
        "banReason": user.ban_reason,
    }

    return payload


def get_user_for_db_test(alt_session, user_id):
    user = get_user_if_exists(alt_session, user_id)
    if not user:
        return None
    else:
        return user


def get_user_for_auth(user_id, request):
    return resolve_user(None, request, user_id)
