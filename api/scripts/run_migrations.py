import alembic.config
import os

alembicArgs = ["--raiseerr", "upgrade", "head"]

current_dir = os.getcwd()
migration_directory = "api/database"

os.chdir(migration_directory)
alembic.config.main(argv=alembicArgs)
os.chdir(current_dir)
