import logging
import tomli
import subprocess
from api.scripts.initial_config import delete_directories, delete_config_file
from api.scripts.create_database import delete_database


def get_packages_to_remove():
    with open("pyproject.toml", "rb") as f:
        toml_dict = tomli.load(f)
        dependencies_dict = toml_dict['tool']['poetry']['dependencies']
        packages = list(dependencies_dict.keys())
        return packages


def remove_packages():
    packages_to_uninstall = str(get_packages_to_remove())
    cmd_str = "poetry remove " + packages_to_uninstall
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
            It will destroy the local database and erase any files inside the created directories
            (which includes any user uploaded files).
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
