import uuid
import json
from api.database.models import User, PasswordReset
from datetime import datetime, timedelta
from api.mail.send_mail import send_email
from starlette.config import environ
import logging
from api.engine import get_engine_from_context
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from os import urandom
from api.auth.crypto import hash_password
from starlette.background import BackgroundTask


def reset_password_request(_, info, email):
    expires = datetime.today() + timedelta(days=1)
    # logging.info("")
    db_engine = get_engine_from_context(info)
    with Session(db_engine) as session:
        try:
            # User
            user = session.scalars(select(User).filter_by(email=email)).one()
            reset_pw_token = uuid.uuid4().hex
            # Add password reset.
            password_reset = PasswordReset(
                user_id=user.id,
                expires=expires,
                token=reset_pw_token,
            )
            session.add(password_reset)
            session.commit()

            # Get mail opts
            mail_opts = json.loads(environ["MAIL"])
            server_opts = json.loads(environ["SERVER"])
            local_mail = mail_opts["local"]
            request = info.context["request"]
            auth_url = server_opts["domain"]
            mail_info = {
                "user": user,
                "url": auth_url,
                "code": password_reset.token,
                "local": local_mail,
                "options": mail_opts,
                "type": "resetpass",
            }
            task = BackgroundTask(send_email, mail_info)
            request.state.background = task
            return True
        except NoResultFound:
            logging.exception(
                "Reset password: User with email {0} does not exist.".format("")
            )
            return True
        except MultipleResultsFound:
            logging.exception(
                "Reset password: Multiple users with email {0} found.".format("")
            )
            return True


def reset_password(_, info, token, password):
    password_reset = session.scalars(
        select(PasswordReset).filter_by(token=token)
    ).one_or_none()
    db_engine = get_engine_from_context(info)
    with Session(db_engine) as session:
        if password_reset is not None:
            user_id = password_reset.user_id
            user = session.scalars(select(User).filter_by(id=user_id)).one_or_none()

            if user is not None:
                # Change password
                salt = urandom(16)  # Generate 16 random bits.
                hashed_pass = hash_password(password, salt)
                user.password = hashed_pass
                user.salt = salt
                session.add(user)
                session.commit()
                return True
            else:
                return False
        else:
            return False
