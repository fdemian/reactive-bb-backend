from rauth import OAuth2Service


def data_to_dict(data):
    return {"email": data["email"], "name": data["name"], "picture": data["picture"]}


# Get facebook oauth user data.
def get_facebook_auth_data(code, service_opts):
    try:
        client = OAuth2Service(
            name=service_opts["name"],
            client_id=service_opts["clientId"],
            client_secret=service_opts["clientSecret"],
            authorize_url=service_opts["authorizeURL"],
            access_token_url=service_opts["accessTokenUrl"],
            base_url=service_opts["baseURL"],
        )
        redirect_uri = "https://www.facebook.com/connect/login_success.html"
        params = {"code": code, "redirect_uri": redirect_uri}
        session = client.get_auth_session(data=params)
        return session.get("me").json()
    except Exception as e:
        print(e)
        return None
