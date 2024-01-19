from api.database.models import User
from api.auth.crypto import hash_password
from os import urandom
from api.resolvers.auth import login_required
from sqlalchemy import select
from sqlalchemy.orm import Session
from api.engine import get_engine_from_context


@login_required
def update_email(_, info, id, email):
    db_engine = get_engine_from_context(info)
    with Session(db_engine) as session:
        user = session.scalars(select(User).filter_by(id=id)).one()
        user.email = email
        session.add(user)
        session.commit()
        return True


@login_required
def update_profile(_, info, id, status, about):
    db_engine = get_engine_from_context(info)
    with Session(db_engine) as session:
        user = session.scalars(select(User).filter_by(id=id)).one()
        user.status = status
        user.about = about
        session.add(user)
        session.commit()

        return {"id": user.id, "ok": True}


@login_required
def update_password(_, info, id, currentPass, newPass):
    salt = urandom(16)  # Generate 16 random bits.
    db_engine = get_engine_from_context(info)
    with Session(db_engine) as session:
        user = session.scalars(select(User).filter_by(id=id)).one()
        current_pass_hash = hash_password(currentPass, user.salt)
        hashed_pass = hash_password(newPass, salt)

        if current_pass_hash == user.password:
            user.password = hashed_pass
            user.salt = salt
            session.add(user)
            session.commit()

            return {"id": user.id, "ok": True}
        else:
            return {"id": 0, "ok": False}
