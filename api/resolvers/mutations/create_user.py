from starlette.background import BackgroundTask
from api.database.models import User, UserActivation
from api.scripts.add_user import do_save_user
from api.mail.send_mail import send_email
from starlette.config import environ
import uuid
import json
import logging
from sqlalchemy.orm import Session
from api.engine import get_engine_from_context
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError


def save_activation_info(activation_code, id, db_session):
    activation_info = UserActivation(user_id=id, token=activation_code)
    db_session.add(activation_info)
    db_session.commit()
    return


def create_user(_, info, username, password, email):
    db_engine = get_engine_from_context(info)
    with Session(db_engine) as session:
        try:
            user_query = session.scalars(
                select(User).filter_by(username=username)
            ).one_or_none()

            if user_query is not None:
                return {"id": 0, "ok": False, "message": "User already exists."}
            else:
                user = {
                    "username": username,
                    "password": password,
                    "email": email,
                    "name": "",
                    "avatar": None,
                    "failed_attempts": 0,
                    "lockout_time": None,
                    "type": "U",
                    "banned": False,
                    "banReason": None,
                }

                mail_opts = json.loads(environ["MAIL"])
                sec_opts = json.loads(environ["SECURITY"])

                local_mail = mail_opts["local"]
                request = info.context["request"]
                server_opts = json.loads(environ["SERVER"])
                auth_url = server_opts["domain"]

                #
                saved_user = do_save_user(user, session, is_valid=False)
                activation_code = str(uuid.uuid4())
                save_activation_info(activation_code, saved_user.id, session)

                if sec_opts["validateMail"]:
                    # Send email as a background task so as not to block for too long.
                    try:
                        mail_info = {
                            "user": saved_user,
                            "url": auth_url,
                            "code": activation_code,
                            "local": local_mail,
                            "options": mail_opts,
                            "type": "activation",
                        }
                        task = BackgroundTask(send_email, mail_info)
                        request.state.background = task
                    except Exception as e:
                        print(e)
                        logging.exception("Exception ocurred")
                        print(":::::")

                return {
                    "ok": True,
                    "id": saved_user.id,
                    "email": saved_user.email,
                    "message": "",
                }
        except SQLAlchemyError:
            session.rollback()
            logging.exception("SQLAlchemy error.")
            return {"ok": False, "id": 0, "email": "", "message": "Generic Error."}
