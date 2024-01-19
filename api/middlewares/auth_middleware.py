import json
from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
    AuthenticationError,
    SimpleUser,
)
from api.auth.auth import validate_token
from starlette.config import environ


# Obtains the access token, wether it is being set directly (in the headers or as a cookie (from the web client).
# TODO: review this...maybe there should be only one way to do this?
def get_access_token(conn):
    token = conn.headers.get("access_token")
    if token is not None:
        return token

    cookie_header = conn.headers.get("cookie")
    if cookie_header is None:
        return None

    cookies = list(
        filter(lambda header: "access_token" in header, cookie_header.split(";"))
    )
    if len(cookies) < 1:
        return None

    auth_cookie = cookies[0].split("=")[1]
    return auth_cookie


class AuthBackend(AuthenticationBackend):
    async def authenticate(self, conn):
        url_path = conn.url.components.path
        if "graphql" not in url_path:
            return

        auth_cookie = get_access_token(conn)
        if auth_cookie is None:
            return

        else:
            try:
                # Get JWT config from settings.
                jwt_config = json.loads(environ["JWT"])
                jwt_settings = jwt_config["auth"]
                secret = jwt_settings["secret"]
                algorithm = jwt_settings["algorithm"]

                # Validate token
                token = validate_token(auth_cookie, secret, algorithm)
                return AuthCredentials(["authenticated"]), SimpleUser(token)

            except Exception:
                raise AuthenticationError("Invalid auth credentials.")
