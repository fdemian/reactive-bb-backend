import json
import logging
import subprocess
from api.scripts.initial_config import create_directories
from api.scripts.initial_config import get_config_opts


def install_packages():
    cmd_str = "poetry install"
    subprocess.run(cmd_str, shell=True)


def get_db_input():
    logging.debug("Getting database input")
    print("====== DATABASE INFO ======")

    # Get inputs
    db_user = input("Database user (default: postgres): ")
    db_password = input("Database password (default: postgres): ")
    db_port = input("Database port (default: 5432): ")
    db_name = input("Database name (default: reactivebb): ")

    return {"user": db_user, "password": db_password, "port": db_port, "name": db_name}


def get_server_input(env):
    port = ""
    server_port = ""
    if env == "DEV" or env == "TEST":
        server_port = input("Enter port (default 8000): ")

    domain = input("Input current domain (default ''):")

    if server_port != "":
        port = int(server_port)

    return {"port": port, "domain": domain}


def replace_config_opts(config_opts, db_input, server_input):
    if server_input["port"] != "":
        config_opts["server"]["port"] = server_input["port"]

    if server_input["domain"] != "":
        config_opts["server"]["domain"] = server_input["domain"]

    if db_input["user"] != "":
        config_opts["database"]["user"] = db_input["user"]

    if db_input["name"] != "":
        config_opts["database"]["name"] = db_input["name"]

    if db_input["port"] != "":
        config_opts["database"]["port"] = db_input["port"]

    if db_input["password"] != "":
        config_opts["database"]["password"] = db_input["password"]
    return config_opts


if __name__ == "__main__":
    # ============== CONFIGURE LOGGER ==============
    logging.basicConfig(
        filename="INSTALLATION.log",
        filemode="a",
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%H:%M:%S",
        level=logging.DEBUG,
    )
    logging.debug("Initializing installation")

    print("============== Initializing installation ==============")

    # ============== GET INFO FROM USER ==============
    """
     Get information from environments by user.
    """

    # Copy correct configuration file.
    print("===== Configuring environment and directories =====")
    logging.debug("Configuring environments")

    environment = ""
    while environment != "DEV" and environment != "PROD" and environment != "TEST":
        environment = input(
            """Select the type of installation: 
          DEV = Development. For local testing.
          PROD = Production. For production environments.
          TEST = Testing. Ideal for running tests. Do not configure in production environments.
          \n\n\n
        """
        )

    # Get database and server input configuration.
    db_input = get_db_input()
    server_input = get_server_input(environment)

    # Get configuration opts for the environment
    logging.debug("Getting configuration file options")
    config_opts = get_config_opts(environment.lower())

    # Get modified config opts and save to file.
    logging.debug("Saving configuration file")

    # ============== SAVE CONFIGURATION FILE ==============

    fixed_config_opts = replace_config_opts(config_opts, db_input, server_input)
    with open("config.json", "w", encoding="utf-8") as f:
        json.dump(fixed_config_opts, f, ensure_ascii=False, indent=4)

    # ============== COMMENCE INSTALLATION ==============
    """
     Here begins the automated part of the installation.
     From here on we won't collect any more information from the user.
    """

    print("===== Installing packages =====")
    logging.debug("Installing packages")
    install_packages()

    # Create directories
    logging.debug("Creating file directories")
    create_directories()

    # Create database
    logging.debug("Creating database")
    from api.scripts.create_database import create_db_and_upgrade
    create_db_and_upgrade()

    # Finished installation
    logging.debug("Installation finished correctly")
    print("===== INSTALLATION COMPLETED =====")
    print("To run the application use the command `python3 start.py`")
    print("To run in the background use `python3 start.py --background true` or `python3 start.py &`")
