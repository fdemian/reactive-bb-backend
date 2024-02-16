import logging
import subprocess
from api.scripts.initial_config import delete_directories, delete_config_file

# TODO: this list of packages should not be maintained manually, since it is too cumbersome to modify.
packages_to_uninstall = "ariadne alembic psycopg2-binary pyjwt starlette python-multipart gunicorn rauth " \
                        "aiohttp aiofiles sqlalchemy-utils websockets graphql-core anyio uvicorn pytest " \
                        "pytest-asyncio pytest-cov coverage broadcaster mypy sqlalchemy asyncpg ruff"


def remove_packages():
    cmd_str = "poetry remove " + packages_to_uninstall
    subprocess.run(cmd_str, shell=True)


def delete_database():
    cmd_str = "poetry run destroydb"
    subprocess.run(cmd_str, shell=True)


if __name__ == "__main__":
    # ============== CONFIGURE LOGGER ==============
    logging.basicConfig(
        filename="UNINSTALL.log",
        filemode="a",
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%H:%M:%S",
        level=logging.DEBUG,
    )
    logging.debug("Uninstalling forum")

    print("============== Uninstalling forum ==============")

    logging.debug("Confirm unistallation environments")

    confirmation = ""
    while confirmation != "Y" and confirmation != "N":
        confirmation = input(
            """WARNING!: This will uninstall the application.
            It will destroy the local database and erase any files inside the created directories (which includes any user uploaded files).
            Are you sure you wish to proceed? (Y/N).
          \n\n\n
        """
        )

    # ============== COMMENCE UNINSTALL ==============
    """
     All uninstallation steps are automated and do not require input from the user.
    """

    # Delete database
    logging.debug("Deleting database")
    delete_database()


    # Remove created directories and all their files.
    logging.debug("Removing file directories")
    delete_directories()

    # Uninstalling packages.
    print("===== Removing packages =====")
    logging.debug("Removing packages")
    remove_packages()

    # Remove configuration files
    logging.debug("Removing configuration file")
    delete_config_file("config.json")

    # Finished installation
    logging.debug("Uninstall finished correctly")
    print("===== UNINSTALL COMPLETED =====")
    print("To reinstall the application use the command `python3 install.py`")

