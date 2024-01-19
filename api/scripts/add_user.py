from sqlalchemy.orm import Session
from getpass import getpass
from api.database.models import User
from api.auth.crypto import hash_password
from os import urandom
from api.database.utils import get_engine


def do_save_user(user_to_save, session, *args, **kwargs):
    """
    Actually save the user.
    """
    # TODO: document this.
    is_valid = kwargs.get("is_valid", None)
    is_oauth = kwargs.get("is_oauth", None)

    salt = urandom(16)  # Generate 16 random bits.
    if not is_oauth:
        hashed_pass = hash_password(user_to_save["password"], salt)
    else:
        hashed_pass = None

    if "banned" in user_to_save:
        ban_status = user_to_save["banned"]
    else:
        ban_status = False

    user = User()
    user.username = user_to_save["username"]
    user.password = hashed_pass
    user.salt = salt
    user.fullname = user_to_save["name"]
    user.email = user_to_save["email"]
    user.failed_attempts = user_to_save["failed_attempts"]
    user.type = user_to_save["type"]
    user.banned = ban_status
    user.ban_reason = user_to_save["banReason"]

    if is_oauth:
        user.avatar = user_to_save["avatar"]
    else:
        user.avatar = None

    if is_valid is None:
        user.valid = False
    else:
        if is_valid is True:
            user.valid = True

    user.valid = is_valid  # A user is not valid until his/her email has ben verified.
    session.add(user)
    session.commit()

    return user


def add_user():
    username = input("Choose a username: ")
    password = getpass("Choose a password: ")
    email = input("Enter a valid email address: ")
    name = input("Choose a user name: ")
    type = input("Choose a user type (A - Admin / M - Moderator / U - Regular user): ")

    user = {
        "username": username,
        "password": password,
        "email": email,
        "name": name,
        "avatar": None,
        "failed_attempts": 0,
        "lockout_time": None,
        "type": type,
        "banned": False,
    }

    db_engine = get_engine()
    with Session(db_engine) as session:
        do_save_user(user, session, is_valid=True)


"""
Initial configuration script.

Creates the initial file upload directories and copies the config file.
"""


def main():
    add_user()
