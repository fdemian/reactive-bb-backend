from os import path
from api.scripts.initial_config import get_config_file_opts

CONFIG_PATH = "../../config.json"
NGINX_CONFIG_FILE_PATH = "../../nginx.sample.conf"
NGINX_CONFIG_FILE_PATH_DEF = "../../ngingx.conf"

current_dir = path.dirname(__file__)
config_file_from = path.join(current_dir, NGINX_CONFIG_FILE_PATH)
config_file_dest = path.join(current_dir, NGINX_CONFIG_FILE_PATH_DEF)
main_config_path = path.join(current_dir, CONFIG_PATH)
PROJECT_PATH = current_dir.split('/api/scripts')[0]


def replace_vars(text: str) -> str:
    config_opts = get_config_file_opts(main_config_path)
    server = config_opts["server"]
    security = config_opts["security"]
    domain = server["domain"]

    return text\
        .replace("<ROOT_DIR>", PROJECT_PATH)\
        .replace("<SSL_CERT_FULLCHAIN>", security['ssl_cert'])\
        .replace("<SSL_CERT_PRIVKEY>", security['ssl_key'])\
        .replace("<SERVER_NAME>", domain)


def generate_conf():
    print("Generating NGINX config file.")
    with open(config_file_from) as reader:
        text = reader.read()
        newtext = replace_vars(text)
        print(newtext)

    with open(config_file_dest, 'w+') as writer:
        writer.write(newtext)
    print("Config file generated.")


def main():
    generate_conf()
