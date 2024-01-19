import json
from starlette.config import environ


def resolve_config(context, info):
    oauth_config = json.loads(environ["OAUTH"])
    oauth_settings = {"services": []}

    if oauth_config["enabled"]:
        oauth_settings["redirectURI"] = oauth_config["redirectURI"]
        for service in oauth_config["services"]:
            oauth_settings["services"].append(
                {
                    "name": service["name"],
                    "scope": service["scope"],
                    "clientId": service["clientId"],
                    "link": service["consentURL"],
                    "extraParams": service["extraParams"],
                }
            )

    return {
        "config": json.loads(environ["CONFIG"]),
        "oauth": json.dumps(oauth_settings),
    }
