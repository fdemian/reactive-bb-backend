from os import path
from api.database.utils import get_database_url_options
from api.utils.utils import parse_config_file
from sqlalchemy_utils import database_exists, drop_database

config_file = "../../config.json"
config_file_path = path.join(path.dirname(__file__), config_file)


def destroy_database():
    options = parse_config_file(config_file_path)
    database_url = get_database_url_options(options)
    if database_exists(database_url):
        drop_database(database_url)


def main():
    destroy_database()
