from os import path, getcwd, fchdir, open, O_RDONLY
from api.read_config import get_database_url_options
from api.utils.utils import parse_config_file
from sqlalchemy_utils import database_exists
from alembic import command
from alembic.config import Config
from .insert_test_data import insert_test_data

# File paths.
config_file = "../../config.json"
config_file_path = path.join(path.dirname(__file__), config_file)
alembic_file_dir = path.join(getcwd(), "api/database")


def run_up_down_migrations(database_url):
    # Change directory.
    fd = open(alembic_file_dir, O_RDONLY)
    fchdir(fd)

    # Set SQL Alchemy URL
    config = Config("alembic.ini")
    config.set_main_option("sqlalchemy.url", database_url)

    # Upgrade command.
    command.downgrade(config, "base")
    command.upgrade(config, "head")


def reset_database():
    options = parse_config_file(config_file_path)
    database_url = get_database_url_options(options)
    if database_exists(database_url):
        run_up_down_migrations(database_url)
        insert_test_data()
    else:
        print("Specified database does not exist.")


def main():
    reset_database()
