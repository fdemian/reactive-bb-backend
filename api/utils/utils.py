import json
import aiofiles
import aiohttp
from time import sleep
import logging


def get_app_state_from_context(info):
    return info.context["request"].app.state


def delay_time(delay_per_try, tries):
    seconds = delay_per_try * tries
    sleep(seconds)
    return


def parse_config_file(config_file_path):
    f = open(config_file_path)
    data = json.load(f)
    return data


async def async_file_read(file_path):
    async with aiofiles.open(file_path, mode="rb") as f:
        contents = await f.read()
        return contents


async def async_json_file_read(file_path):
    async with aiofiles.open(file_path, mode="r") as f:
        contents = await f.read()

    data = json.loads(contents)
    return data


async def async_file_download(url, destination):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                f = await aiofiles.open(destination, mode="wb")
                await f.write(await resp.read())
                await f.close()


def file_download(url):
    with aiohttp.ClientSession() as session:
        with session.get(url) as resp:
            data = resp.json()
            return data


def save_file(path, data):
    with open(path, "bw") as f:
        f.write(data)


# Logs the parameters of a request (I.E) the GraphQL query and its variables.
async def log_request(info):
    logger = logging.getLogger("admin.graphql")
    body_b = await info.context["request"].body()
    logger.info(str(body_b.decode("UTF-8")))
