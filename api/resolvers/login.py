import json
import logging
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from sqlalchemy import select
from sqlalchemy.orm import Session
from api.database.models import User
from api.utils.utils import delay_time
from api.auth.crypto import check_password, hash_password
from api.auth.auth import user_to_dict
from api.resolvers.auth import auth_flow_response
from datetime import datetime
from starlette.responses import JSONResponse
from starlette.config import environ
from api.engine import get_engine_from_request
from sqlalchemy.engine import Engine

"""
set_cookie / params:

* key (str) – the key (name) of the cookie to be set.
* value (str) – the value of the cookie.
* max_age (Optional[Union[datetime.timedelta, int]]) – should be a number of seconds, or None (default) if the cookie should last only as long as the client’s browser session.
* expires (Optional[Union[str, datetime.datetime, int, float]]) – should be a datetime object or UNIX timestamp.
* path (Optional[str]) – limits the cookie to a given path, per default it will span the whole domain.
* domain (Optional[str]) – if you want to set a cross-domain cookie. For example, domain=".example.com" will set a cookie that is readable by the domain www.example.com, foo.example.com etc. Otherwise, a cookie will only be readable by the domain that set it.
* secure (bool) – If True, the cookie will only be available via HTTPS.
* httponly (bool) – Disallow JavaScript access to the cookie.
* samesite (Optional[str]) – Limit the scope of the cookie to only be attached to requests that are “same-site”.

Params to set in the future.
 * secure (only with HTTPS)
 * samesite (set to the current site)
 * max_age / expires
"""


async def logout(request) -> JSONResponse:
    response = JSONResponse({"ok": True})
    response.delete_cookie("access_token", path="/", domain=None)
    response.delete_cookie("refresh_token", path="/", domain=None)
    return response


async def login(request):
    body = await request.json()
    username = body["username"]
    password = body["password"]

    # Try to authenticate user.
    jwt_settings = json.loads(environ["JWT"])
    db_engine = get_engine_from_request(request)
    user = authenticate_user(username, password, db_engine)
    return auth_flow_response(user, jwt_settings)


def check_ban_expiration(exp_date):
    if exp_date is None:
        return False
    return exp_date.date() >= datetime.today().date()


def authenticate_user(
    username: str, password: str, db_engine: Engine
) -> dict[str, str] | None:
    logger = logging.getLogger("admin.graphql")
    logger.info(f"Login requested for user: {username}.")
    with Session(db_engine) as session:
        password_is_correct = False
        account_settings = json.loads(environ["ACCOUNT"])
        max_login_tries = int(account_settings["maxLoginTries"])
        login_delay = int(account_settings["loginDelayTimeStep"])
        lockout_time = int(account_settings["lockoutTimeWindow"])

        user = get_user_if_exists(session, username)

        if user is None:
            logger.info(f"Requested nonexistent user: {username}")
            user = get_mock_user()
            hash_password("*****", b"")
            user_exists = False
        else:
            # logger.info("User exists and is: " + username)
            # logger.info(user.failed_attempts)
            user_exists = True
            if user.failed_attempts > 0:
                # Wait an amount of time proportional to the number of failed attempts.
                delay_time(login_delay, user.failed_attempts)

            check_pass = check_password(password, user.password, user.salt)

            # User tried to log in the maximum number of allowed tries.
            if user_is_locked(session, user, lockout_time):
                logger.error(
                    f"User: {username} is locked. Too many failed attempts have been made."
                )
                return None

            """
             If the user is valid and it exists verify that the password was input correctly.
             If not, register the failed attempt in the database.
            """
            if user.valid and user_exists:
                if check_pass:
                    password_is_correct = True
                    if user.failed_attempts > 0:
                        unlock_user(session, user)
                else:
                    logger.error(
                        f"Failed attempt: {username} tried to log in with the wrong password."
                    )
                    password_is_correct = False
                    register_failed_login(session, user, max_login_tries)
            else:
                password_is_correct = False

            if password_is_correct:
                user_dict = user_to_dict(user)
                if user.banned and check_ban_expiration(user.ban_expires):
                    logger.error(f"User ban expired for user: {username}.")
                    unban_user(session, user)
                logger.info(f"Login successful for user: {username}.")
                return user_dict
            else:
                return None
    return None


# ========================== UTILITY FUNCTIONS ========================== #


def get_mock_user() -> User:
    mock_user = User()
    mock_user.username = "fakeuser"
    mock_user.password = hash_password("fake_password", b"")
    mock_user.banned = False
    mock_user.ban_reason = None
    mock_user.ban_expires = None
    mock_user.lockout_time = None
    mock_user.failed_attempts = 0
    mock_user.email = "fake@fake.com"
    mock_user.type = "U"
    mock_user.fullname = "Fake Mega User"
    mock_user.valid = False
    return mock_user


def get_user_if_exists(session: Session, username: str) -> None | User:
    try:
        user = session.scalars(select(User).filter_by(username=username)).one()
        return user
    except MultipleResultsFound:
        print("MultipleResultsFound")
        return None
    except NoResultFound:
        print("NoResultFound")
        return None


def user_is_locked(session: Session, user: User, lockout_time: int) -> bool:
    if user.lockout_time is None:
        return False

    time_elapsed: datetime = datetime.now() - user.lockout_time
    if time_elapsed.seconds > (lockout_time * 60):
        unlock_user(session, user)
        return False
    else:
        return True


def unlock_user(session: Session, user: User) -> None:
    user.failed_attempts = 0
    user.lockout_time = None
    session.merge(user)
    session.commit()
    return


def unban_user(session: Session, user: User) -> None:
    user.banned = False
    user.ban_expires = None
    user.ban_reason = None
    session.add(user)
    session.commit()
    return


def register_failed_login(session: Session, user: User, max_login_tries: int) -> User:
    user.failed_attempts = user.failed_attempts + 1

    # If the user reached the maximum number of tries.
    if user.failed_attempts is max_login_tries:
        user.lockout_time = datetime.now()

    session.merge(user)
    session.commit()

    return user
