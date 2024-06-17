import shutil
import json
from os import path, mkdir, remove
from os.path import isdir
from shutil import rmtree

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
    avatars_dir = path.join(path.join(root_path, "static"), "avatars")
    uploads_dir = path.join(path.join(root_path, "static"), "uploads")

    if not isdir(uploads_dir):
        mkdir(uploads_dir)

    if not isdir(avatars_dir):
        mkdir(avatars_dir)


def delete_directories():

    uploads_dir = path.join(root_path, "uploads")
    avatars_dir = path.join(path.join(root_path, "static"), "avatars")

    if isdir(uploads_dir):
        rmtree(uploads_dir)

    if isdir(avatars_dir):
        rmtree(avatars_dir)


def delete_config_file(config_file_path):
    if path.isfile(config_file_path):
        remove(config_file_path)


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
