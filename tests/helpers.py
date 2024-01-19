from api.database.models import UserActivation, User, PasswordReset
from sqlalchemy import select
from sqlalchemy.orm import Session
from api.database.utils import get_engine


def get_activation_token(email: str) -> str:
    db_engine = get_engine()
    with Session(db_engine) as session:
        user: User = session.scalars(select(User).filter_by(email=email)).one()
        user_activation: UserActivation = session.scalars(
            select(UserActivation).filter_by(user_id=user.id)
        ).one()
        return user_activation.token


def get_password(user_id: int):
    db_engine = get_engine()
    with Session(db_engine) as session:
        user = session.scalars(select(User).filter_by(id=user_id)).one()
        return {"password": user.password, "salt": user.salt}


def get_user_reset_token(email: str) -> str:
    db_engine = get_engine()
    with Session(db_engine) as session:
        user: User = session.scalars(select(User).filter_by(email=email)).one()
        pw_reset_info: PasswordReset = session.scalars(
            select(PasswordReset).filter_by(user_id=user.id)
        ).one()
        return pw_reset_info.token
