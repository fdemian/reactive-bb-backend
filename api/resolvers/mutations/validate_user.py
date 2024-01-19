from api.database.models import User, UserActivation
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.orm import Session
from sqlalchemy import select
from api.engine import get_engine_from_context


def validate_user(_, info, token):
    db_engine = get_engine_from_context(info)
    with Session(db_engine) as session:
        try:
            user_activation = session.scalars(
                select(UserActivation).filter_by(token=token)
            ).one()
            user_to_validate = session.scalars(
                select(User).filter_by(id=user_activation.user_id)
            ).one()

            user_to_validate.valid = True
            session.commit()
            session.flush()

            session.delete(user_activation)
            session.commit()

            return {"id": user_to_validate.id, "ok": True}

        except (NoResultFound, MultipleResultsFound):
            return {"id": 0, "ok": False}
