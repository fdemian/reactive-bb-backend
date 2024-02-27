# Reactive BB (Backend)

Reactive BB is a modern forum application for the next generation. 
This repository houses the backend of the application.

# Installation instructions

## Prerrequisites 

The following packages must be installed on the target machine for the application to run correctly.

- [Python](https://www.python.org/) (Pick a version >= 3.11)
- [Poetry](https://python-poetry.org/)
- [PostgreSQL](https://www.postgresql.org/)

## Installation

1) Run the installation script and fill in the necessary information:

`poetry run python3.11 install.py`

The script will ask you for information, generate the config files, create the database and associated directories.

2) Once you have run the installation script, you will have created an empty application. Create some users by running the following commands.

`poetry run adduser`

You will be prompted to input the user name, password, and role.

## How to run 

Run the application in foreground mode.

`python3 start.py`

Run the application in background mode

`python3 start.py --background true` or `python3 start.py &`

### Static check

`poetry run ruff check .` # Lint all files in the current directory (and any subdirectories).

### Run static type checker

`poetry run mypy`

# Technologies 

This backend is written in python and uses the following technologies:

- [Poetry](https://python-poetry.org/) (Package management)
- [Starlette](https://www.starlette.io/) (Application server)
- [Uvicorn](https://www.uvicorn.org/) (Web server)
- [Ariadne](https://ariadnegraphql.org/) (Graphql library)
- [SQLAlchemy](https://www.sqlalchemy.org/) (Graphql library)
- [PostgreSQL](https://www.postgresql.org/) (Database engine)