import json
from functools import wraps
from api.auth.auth import get_user_tokens
from api.resolvers.queries.user import get_user_for_auth
from starlette.responses import JSONResponse
from starlette.authentication import AuthenticationError
from starlette.config import environ


def auth_flow_response(user, jwt_settings):
    """
    * set_cookie params:
    *
    * key (str) – the key (name) of the cookie to be set.
    * value (str) – the value of the cookie.
    * max_age (Optional[Union[datetime.timedelta, int]]) – should be a number of seconds, or None (default) if the cookie should last only as long as the client’s browser session.
    * expires (Optional[Union[str, datetime.datetime, int, float]]) – should be a datetime object or UNIX timestamp.
    * path (Optional[str]) – limits the cookie to a given path, per default it will span the whole domain.
    * domain (Optional[str]) – if you want to set a cross-domain cookie. For example, domain=".example.com" will set a cookie that is readable by the domain www.example.com, foo.example.com etc. Otherwise, a cookie will only be readable by the domain that set it.
    * secure (bool) – If True, the cookie will only be available via HTTPS.
    * httponly (bool) – Disallow JavaScript access to the cookie.
    * samesite (Optional[str]) – Limit the scope of the cookie to only be attached to requests that are “same-site”.
    """

    if user is None:
        return JSONResponse(
            {
                "ok": False,
                "ttl": "",
                "id": None,
                "banned": False,
                "banReason": None,
                "banExpirationTime": None,
            }
        )

    jwt_token = get_user_tokens(user, jwt_settings)
    auth_expiration = jwt_settings["auth"]["expiration"]
    refresh_expiration = jwt_settings["refresh"]["expiration"]
    server_opts = json.loads(environ["SERVER"])
    is_prod = bool(server_opts["production"])
    #domain = None
    samesite = "lax"
    if is_prod:
        samesite = "strict"
        #domain = server_opts["domain"]
    try:
        response = JSONResponse(
            {
                "ok": True,
                "ttl": auth_expiration,
                "banned": user["banned"],
                "banReason": user["banReason"],
                "banExpirationTime": user["banExpirationTime"],
                "type": user["type"],
                "id": user["id"],
            }
        )
        response.set_cookie(
            "access_token",
            jwt_token["auth"],
            max_age=None,
            expires=auth_expiration,
            secure=is_prod,
            httponly=True,
            samesite=samesite,
        )
        response.set_cookie(
            "refresh_token",
            jwt_token["refresh"],
            max_age=None,
            expires=refresh_expiration,
            secure=is_prod,
            httponly=True,
            samesite=samesite,
        )
        return response
    except:
        print(f"Unknown Error - {sys.exc_info()[1]}")
        print(f"Details - {sys.exc_info()}")
        return JSONResponse(
            {
                "ok": False,
                "ttl": "",
                "id": None,
                "banned": False,
                "banReason": None,
                "banExpirationtTime": None,
            }
        )


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        request = args[1].context["request"]
        if request.user.is_authenticated:
            return f(*args, **kwargs)
        else:
            raise AuthenticationError("Invalid auth credentials.")

    return decorated_function


# Both mod and admin can access this validation.
def mod_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        request = args[1].context["request"]
        if request.user.is_authenticated:
            user_id = request.user.display_name["user_token"]
            user = get_user_for_auth(user_id)
            if user.type == "M" or user.type == "A":
                return f(*args, **kwargs)
            else:
                raise AuthenticationError("Invalid permissions")
        else:
            raise AuthenticationError("Invalid auth credentials")

    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        request = args[1].context["request"]
        if request.user.is_authenticated:
            user_id = request.user.display_name["user_token"]
            user = get_user_for_auth(user_id)
            if user.type == "A":
                return f(*args, **kwargs)
            else:
                raise AuthenticationError("Invalid permissions")
        else:
            raise AuthenticationError("Invalid auth credentials")

    return decorated_function
