import json
from api.auth.auth import validate_token
from api.auth.auth import get_user_tokens
from starlette.responses import JSONResponse
from starlette.authentication import AuthenticationError
from starlette.config import environ


def get_resfresh_token(request):
    token = request.headers.get("access_token")
    if token is not None:
        return token
    ref_token = request.cookies.get("refresh_token")
    return ref_token


async def refresh_tokens(request):
    ref_token = get_resfresh_token(request)
    jwt_settings = json.loads(environ["JWT"])

    secret = jwt_settings["refresh"]["secret"]
    algorithm = jwt_settings["refresh"]["algorithm"]
    auth_expiration = jwt_settings["auth"]["expiration"]
    refresh_expiration = jwt_settings["refresh"]["expiration"]

    token = validate_token(ref_token, secret, algorithm)

    if token is not None:
        user = {"id": token["user_token"]}
        new_tokens = get_user_tokens(user, jwt_settings)
        res = JSONResponse({"ok": True, "ttl": auth_expiration, "id": user["id"]})
        res.set_cookie(
            "access_token",
            new_tokens["auth"],
            max_age=None,
            expires=auth_expiration,
            path="/",
            domain=None,
            secure=False,
            httponly=True,
            samesite="lax",
        )
        res.set_cookie(
            "refresh_token",
            new_tokens["refresh"],
            max_age=None,
            expires=refresh_expiration,
            path="/",
            domain=None,
            secure=False,
            httponly=True,
            samesite="lax",
        )

        return res

    else:
        raise AuthenticationError("Invalid auth credentials.")
