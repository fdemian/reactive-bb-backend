import json
import logging
from starlette.config import environ
from os import path
from api.utils.utils import async_json_file_read, parse_config_file

config_file = "../config.json"
config_file_path = path.join(path.dirname(__file__), config_file)


def config_to_environ_sync(**kwargs) -> None:
    config_json = parse_config_file(config_file_path)
    try:
        environ["ENVIRON"] = config_json["environment"]
        environ["DATABASE"] = json.dumps(config_json["database"])
        environ["SERVER"] = json.dumps(config_json["server"])
        environ["ACCOUNT"] = json.dumps(config_json["account"])
        environ["JWT"] = json.dumps(config_json["jwt"])
        environ["CONFIG"] = json.dumps(config_json["forum"])
        environ["MAIL"] = json.dumps(config_json["mail"])
        environ["SECURITY"] = json.dumps(config_json["security"])
        environ["OAUTH"] = json.dumps(config_json["oauth"])
        if kwargs.get("testing") is not None:
            environ["TESTING"] = "True"
    except:
        logger = logging.getLogger("admin.graphql")
        logger.error("[READ CONFIG ERROR]")

    return


async def config_to_environ(**kwargs) -> None:
    config_json = await async_json_file_read(config_file_path)
    try:
        environ["ENVIRON"] = config_json["environment"]
        environ["DATABASE"] = json.dumps(config_json["database"])
        environ["SERVER"] = json.dumps(config_json["server"])
        environ["ACCOUNT"] = json.dumps(config_json["account"])
        environ["JWT"] = json.dumps(config_json["jwt"])
        environ["CONFIG"] = json.dumps(config_json["forum"])
        environ["MAIL"] = json.dumps(config_json["mail"])
        environ["SECURITY"] = json.dumps(config_json["security"])
        environ["OAUTH"] = json.dumps(config_json["oauth"])
    except:
        logger = logging.getLogger("admin.graphql")
        logger.info("[READ CONFIG ERROR]")
    return
