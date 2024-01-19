from rauth import OAuth2Service


def data_to_dict(data):
    return {
        "email": data["email"],
        "name": data["login"],
        "picture": data["avatar_url"],
    }


# Get google oauth user data.
def get_github_auth_data(code, redirect_uri_base, service_opts):
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
        gh_session = client.get_auth_session(data=data)
        user_data = gh_session.get(
            "https://api.github.com/user", params={"format": "json", code: code}
        )
        return data_to_dict(user_data.json())
    except Exception as e:
        print(e)
        return None
