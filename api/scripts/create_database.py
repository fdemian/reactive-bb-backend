from os import path, getcwd, fchdir, open, O_RDONLY
from api.database.utils import get_database_url_options
from api.utils.utils import parse_config_file
from sqlalchemy_utils import database_exists, create_database, drop_database
from alembic import command
from alembic.config import Config

# File paths.
config_file = "../../config.json"
config_file_path = path.join(path.dirname(__file__), config_file)
alembic_file_dir = path.join(getcwd(), "api/database")


def run_migrations(database_url):
    if database_exists(database_url):
        fd = open(alembic_file_dir, O_RDONLY)
        fchdir(fd)
        config = Config("alembic.ini")
        config.set_main_option("sqlalchemy.url", database_url)
        command.upgrade(config, "head")


def create_database_if_not_exists(database_url):
    if not database_exists(database_url):
        create_database(database_url)


def delete_database():
    options = parse_config_file(config_file_path)
    database_url = get_database_url_options(options)
    drop_database(database_url.render_as_string(hide_password=False))


def create_db_and_upgrade():
    options = parse_config_file(config_file_path)
    database_url = get_database_url_options(options)
    create_database_if_not_exists(database_url)
    run_migrations(database_url.render_as_string(hide_password=False))


def main():
    create_db_and_upgrade()
