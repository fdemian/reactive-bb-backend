import os
import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy_utils import database_exists, create_database, drop_database
from api.read_config import config_to_environ
from api.database.utils import get_database_url

ALEMBIC_PATH = "api/database"
ALEMBIC_CONFIG_PATH = os.path.join(ALEMBIC_PATH, "alembic.ini")


# Test database.
@pytest.mark.asyncio
async def test_create_and_destroy_database():
    await config_to_environ(testing=True)

    # Set up database url and configuration.
    database_url = get_database_url()

    config = Config(ALEMBIC_CONFIG_PATH)  # Run the migrations.
    config.set_main_option(
        "sqlalchemy.url", database_url.render_as_string(hide_password=False)
    )
    config.set_main_option("script_location", os.path.join(ALEMBIC_PATH, "alembic"))
    assert (
        config.get_main_option("script_location") is not None
    ), "Script location variable does not exist."

    if database_exists(database_url):
        drop_database(database_url)  # Drop the test database.

    assert not database_exists(database_url), "Test database already exists."
    create_database(database_url)  # Create the test database.
    assert database_exists(database_url), "Test database not created successfully."
    command.upgrade(config, "head")
    command.downgrade(config, "base")
    command.upgrade(config, "head")

    # Insert test data.
    from api.scripts.insert_test_data import insert_test_data_db

    insert_test_data_db()

    if database_exists(database_url):
        drop_database(database_url)  # Drop the test database.
    assert not database_exists(
        database_url
    ), "Test database not destroyed successfully."
