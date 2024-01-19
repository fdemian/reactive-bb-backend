import jwt
from datetime import datetime, timedelta
from starlette.authentication import AuthenticationError

"""
TODO: GENERATE TOKEN. LOOK AT:
https://hoangdinhquang.me/a-note-on-jwt-and-csrf-attack/
OR
https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html#verifying-origin-with-standard-headers
"""


def generate_token(user, jwt_settings):
    expiration_time = int(jwt_settings["expiration"])
    secret = jwt_settings["secret"]
    expdate = datetime.utcnow() + timedelta(seconds=expiration_time)
    jwt_payload = {"user_token": user, "exp": expdate}
    jwt_token = jwt.encode(jwt_payload, secret, algorithm=jwt_settings["algorithm"])

    return jwt_token


# Helper method (move?)
def get_user_tokens(user, jwt_settings):
    user_token = str(user["id"])
    auth_token = generate_token(user_token, jwt_settings["auth"])
    refresh_token = generate_token(user_token, jwt_settings["refresh"])

    return {"auth": auth_token, "refresh": refresh_token}


# Decode a JWT token and return the results.
def validate_token(jwt_token, secret, algorithm):
    try:
        if jwt_token is None:
            return None

        verify_options = {"verify_signature": True, "verify_exp": True}
        payload = jwt.decode(
            jwt_token, secret, algorithms=[algorithm], options=verify_options
        )
        return payload

    except (jwt.DecodeError, jwt.ExpiredSignatureError):
        raise AuthenticationError("Invalid auth credentials.")


def user_to_dict(user):
    user_link = "/users/" + str(user.id) + "/" + user.username

    payload = {
        "id": user.id,
        "avatar": user.avatar,
        "username": user.username,
        "fullname": user.fullname,
        "email": user.email,
        "banned": user.banned,
        "banReason": user.ban_reason,
        "banExpirationTime": user.ban_expires,
        "type": user.type,
        "link": user_link,
    }

    return payload
