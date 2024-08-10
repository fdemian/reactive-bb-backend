from api.database.utils import get_engine
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from sqlalchemy import select
from sqlalchemy.orm import Session
from api.database.models import User


def delete_all_instances(session: Session, username: str) -> None:
    users = session.scalars(select(User).filter_by(username=username)).all()
    for user in users:
        session.delete(user)
    session.commit()


def delete_user():
    from api.read_config import config_to_environ_sync

    config_to_environ_sync()

    username = input("Specify username to delete: ")
    db_engine = get_engine()
    with Session(db_engine) as session:
        delete_all_instances(session, username)


"""
Initial configuration script.

Creates the initial file upload directories and copies the config file.
"""


def main():
    delete_user()
