import json
from rauth import OAuth2Service


def data_to_dict(data):
    return {"email": data["email"], "name": data["name"], "picture": data["picture"]}


# Keep this url in case google's URLs change.
# https://accounts.google.com/.well-known/openid-configuration
def get_google_auth_data(code, redirect_uri_base, service_opts):
    # Get google oauth user data.
    try:
        client = OAuth2Service(
            name=service_opts["name"],
            client_id=service_opts["clientId"],
            client_secret=service_opts["clientSecret"],
            authorize_url=service_opts["authorizeURL"],
            access_token_url=service_opts["accessTokenUrl"],
            base_url=service_opts["baseURL"],
        )

        data = dict(
            code=code,
            redirect_uri=redirect_uri_base + "/oauth/" + service_opts["name"],
            grant_type="authorization_code",
        )
        gg_session = client.get_auth_session(data=data, decoder=json.loads)
        session_data = gg_session.get(
            "https://www.googleapis.com/oauth2/v1/userinfo", params={"format": "json"}
        )
        return data_to_dict(session_data.json())
    except Exception as e:
        print(e)
        return None
