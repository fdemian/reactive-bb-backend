import os
import pytest
from alembic import command
from alembic.config import Config
from api.read_config import config_to_environ, config_to_environ_sync
from sqlalchemy_utils import database_exists, create_database, drop_database
from sqlalchemy.orm import Session
from starlette.testclient import TestClient
from api.database.utils import get_database_url

#
from api.database.utils import get_engine
from broadcaster import Broadcast


ALEMBIC_PATH = "api/database"
ALEMBIC_CONFIG_PATH = os.path.join(ALEMBIC_PATH, "alembic.ini")


@pytest.hookimpl(hookwrapper=False)
def pytest_exception_interact(node, call, report):
    config_to_env_sync(testing=True)
    database_url = get_database_url()
    if report.failed:
        # call.excinfo contains an ExceptionInfo instance
        if database_exists(database_url):
            drop_database(database_url)
            yield


async def get_test_client():
    await config_to_environ(testing=True)
    from api.app import get_main_app

    app = get_main_app()
    broadcast = Broadcast("memory://")
    await broadcast.connect()
    engine = get_engine()
    app.state.engine = engine
    app.state.broadcast = broadcast
    return TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """
    Create a clean test database with data.
    """
    config_to_environ_sync(testing=True)
    database_url = get_database_url().render_as_string(hide_password=False)
    from api.database.utils import get_engine
    from api.scripts.insert_test_data import insert_test_data_db
    from api.resolvers.queries.user import get_user_for_db_test

    config = Config(ALEMBIC_CONFIG_PATH)  # Run the migrations.
    config.set_main_option("sqlalchemy.url", database_url)
    config.set_main_option("script_location", os.path.join(ALEMBIC_PATH, "alembic"))

    assert (
        config.get_main_option("script_location") is not None
    ), "Script location variable does not exist."

    if database_exists(database_url):
        drop_database(database_url)

    assert not database_exists(
        database_url
    ), "Test database already exists. Aborting tests."
    create_database(database_url)  # Create the test database.
    assert database_exists(database_url), "Test database not created successfully."
    command.upgrade(config, "head")
    inserted_user_id = insert_test_data_db()
    engine = get_engine()
    with Session(engine) as alt_session:
        user = get_user_for_db_test(alt_session, inserted_user_id)
        assert user is not None
        assert user.id == 1
    yield
    if database_exists(database_url):
        drop_database(database_url)  # Drop the test database.
