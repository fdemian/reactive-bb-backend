import shutil
import json
from os import path, mkdir
from os.path import isdir

config_dir = "../../config"
config_dir_path = path.join(path.dirname(__file__), config_dir)

dest_dir = "../.."
dest_dir_path = path.join(path.dirname(__file__), dest_dir)

root_dir = "../../"
root_path = path.join(path.dirname(__file__), root_dir)


def create_directories():
    """
    Create directories:
      - uploads (general file / images uploads)
      - avatars (`static/avatars` user avatars). This is the default folder where user avatars are placed.
    """

    uploads_dir = path.join(root_path, "uploads")
    avatars_dir = path.join(path.join(root_path, "static"), "avatars")

    if not isdir(uploads_dir):
        mkdir(uploads_dir)

    if not isdir(avatars_dir):
        mkdir(avatars_dir)


def copy_config_file(env):
    """
    Copy the configuration file to the root directory.
    """
    source = path.join(config_dir_path, f"config.{env}.json")
    dest = path.join(dest_dir_path, "config.json")
    shutil.copyfile(source, dest)


def get_config_opts(env):
    source_config = path.join(config_dir_path, f"config.{env}.json")
    with open(source_config) as user_file:
        parsed_json = json.load(user_file)
        return parsed_json


def main():
    """
    Initial configuration script.

    Creates the initial file upload directories and copies the config file.
    """
    copy_config_file("prod")
    create_directories()
