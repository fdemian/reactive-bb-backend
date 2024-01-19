import json
from sqlalchemy import create_engine, URL
from starlette.config import environ
from api.utils.utils import parse_config_file


def get_url_object(database_conf, db_name):
    url_object = URL.create(
        f"postgresql+{database_conf['driver']}",
        username=database_conf["user"],
        password=database_conf["password"],
        host="localhost",
        port=database_conf["port"],
        database=db_name,
    )
    return url_object


def get_database_url() -> URL:
    database_conf = json.loads(environ["DATABASE"])
    testing = "TESTING" in environ and environ["TESTING"] == "True"
    if testing:
        db_name = database_conf["name"] + "__test"
    else:
        db_name = database_conf["name"]

    url_object = URL.create(
        f"postgresql+{database_conf['driver']}",
        username=database_conf["user"],
        password=database_conf["password"],
        host="localhost",
        port=database_conf["port"],
        database=db_name,
    )
    return url_object


def get_engine():
    connection_url = get_database_url()
    if "TESTING" in environ:
        connnect_args = {
            "keepalives": 1,
            "keepalives_idle": 30,
            "keepalives_interval": 10,
            "keepalives_count": 5,
        }
        engine = create_engine(
            connection_url, pool_pre_ping=True, connect_args=connnect_args
        )
    else:
        engine = create_engine(connection_url)
    return engine


def get_database_url_options(options):
    url_object = URL.create(
        f"postgresql+{options['database']['driver']}",
        username=options["database"]["user"],
        password=options["database"]["password"],
        host="localhost",
        port=options["database"]["port"],
        database=options["database"]["name"],
    )
    return url_object


def get_database_url_from_config_file(config_file_path):
    options = parse_config_file(config_file_path)
    testing = "TESTING" in environ and environ["TESTING"] == "True"
    if testing:
        db_name = options["database"]["name"] + "__test"
    else:
        db_name = options["database"]["name"]

    url_object = URL.create(
        f"postgresql+{options['database']['driver']}",
        username=options["database"]["user"],
        password=options["database"]["password"],
        host="localhost",
        port=options["database"]["port"],
        database=db_name,
    )
    return url_object
