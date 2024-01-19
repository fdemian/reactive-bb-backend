import json


def data_to_dict(data):
    return {"email": data["email"], "name": data["name"], "picture": data["picture"]}


# Keep this url in case google's URLs change.
# https://accounts.google.com/.well-known/openid-configuration
def get_twitter_auth_data(code):
    # Get google oauth user data.
    client_id = ""
    client_secret = ""
    try:
        client = OAuth2Service(
            name="twitter",
            authorize_url="https://accounts.google.com/o/oauth2/auth",
            access_token_url="https://accounts.google.com/o/oauth2/token",
            client_id=client_id,
            client_secret=client_secret,
            base_url="https://accounts.google.com/o/oauth2/auth",
        )

        data = dict(
            code=code,
            redirect_uri="https://www.fdemian.com/oauth/google",
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
