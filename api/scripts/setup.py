from .create_database import create_db_and_upgrade
from .initial_config import create_directories


# Setup script: create directories and and database.
def main():
    create_directories()
    create_db_and_upgrade()
