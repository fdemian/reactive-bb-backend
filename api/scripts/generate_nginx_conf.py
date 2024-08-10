from api.database.utils import get_engine
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from sqlalchemy import select
from sqlalchemy.orm import Session
from api.database.models import User
from os import path

NGINX_CONFIG_FILE_PATH = "../../nginx.sample.conf"
NGINX_CONFIG_FILE_PATH_DEF = "../../ngingx.conf"

current_dir = path.dirname(__file__)
config_file_from = path.join(current_dir, NGINX_CONFIG_FILE_PATH)
config_file_dest = path.join(current_dir, NGINX_CONFIG_FILE_PATH_DEF)
PROJECT_PATH = current_dir.split('/api/scripts')[0]


def replace_vars(text: str) -> str:
    return text\
        .replace("<ROOT_DIR>", PROJECT_PATH)\
        .replace("<SSL_CERT_FULLCHAIN>", "FULL_CHAIN")\
        .replace("<SSL_CERT_PRIVKEY>", "FULL_KEY")\
        .replace("<SERVER_NAME>", "HTTP_DOMAIN")


def generate_conf():
    from api.read_config import config_to_environ_sync

    config_to_environ_sync()
    print("Generating NGINX config file: ")
    print()
    with open(config_file_from) as reader:
        text = reader.read()
        newtext = replace_vars(text)
        print(newtext)

    with open(config_file_dest, 'w+') as writer:
        writer.write(newtext)

"""
Initial configuration script.

Creates the initial file upload directories and copies the config file.
"""


def main():
    generate_conf()
