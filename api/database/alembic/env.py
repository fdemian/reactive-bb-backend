from logging.config import fileConfig
from api.database.utils import get_database_url_from_config_file
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from os.path import exists

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = None

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

config_file = "../../config.json"
config_file_alt = "./config.json"


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    file_path = ""
    if exists(config_file):
        file_path = config_file
    else:
        file_path = config_file_alt

    url = get_database_url_from_config_file(file_path)
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    file_path = ""
    if exists(config_file):
        file_path = config_file
    else:
        file_path = config_file_alt
    config_section = config.get_section(config.config_ini_section)
    url = get_database_url_from_config_file(file_path)

    """
    if 'TESTING' in environ and environ['TESTING'] == 'True':
        print(url)
        url = url + '__test'
    """

    config_section["sqlalchemy.url"] = url
    connectable = engine_from_config(
        config_section,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
