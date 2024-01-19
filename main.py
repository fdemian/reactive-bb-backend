import json
import uvicorn
import asyncio
from api.read_config import config_to_environ
from starlette.config import environ
from typing import Any


async def main() -> None:
    await config_to_environ()
    server_conf: dict[str, Any] = json.loads(environ["SERVER"])
    environment: str = environ["ENVIRON"]
    port: int = int(server_conf["port"])
    socket_name: str = server_conf["sockName"]

    # MAIN APP
    from api.app import get_main_app

    main_app = get_main_app()

    # Configure main app.
    if environment == "development":
        config = uvicorn.Config(
            main_app, port=port, log_level="info", log_config="log.json"
        )
    else:
        config = uvicorn.Config(
            main_app, uds=socket_name, log_level="info", log_config="log.json"
        )

    server: uvicorn.Server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
