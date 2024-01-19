import json
from os import path, getcwd
from api.auth.auth import user_to_dict
from api.utils.utils import async_file_download
from api.database.models import User
from api.scripts.add_user import do_save_user
from api.resolvers.auth import auth_flow_response
from api.resolvers.oauthservices.google import get_google_auth_data
from api.resolvers.oauthservices.github import get_github_auth_data
from starlette.responses import JSONResponse
from starlette.config import environ
from sqlalchemy.orm import Session
from api.engine import get_engine_from_request


service_data_functions = {
    "google": get_google_auth_data,
    "github": get_github_auth_data,
}


async def oauth(request):
    db_engine = get_engine_from_request(request)
    with Session(db_engine) as session:
        try:
            body = await request.json()
            service = body["service"]
            code = body["code"]
            jwt_settings = json.loads(environ["JWT"])
            oauth_settings = json.loads(environ["OAUTH"])

            if not oauth_settings["enabled"]:
                return JSONResponse({"ok": False, "ttl": "", "id": None})

            # Service auth path.
            redirect_uri_base = oauth_settings["redirectURI"]
            service_opts = next(
                filter(lambda s: s["name"] == service, oauth_settings["services"])
            )
            get_auth_data = service_data_functions[service]
            json_data = get_auth_data(code, redirect_uri_base, service_opts)

            email = json_data["email"]
            name = json_data["name"]
            picture = json_data["picture"]
            user_query = session.query(User).filter(User.email == email).one_or_none()

            # User already exists. Do not save it in the database.
            if user_query is not None:
                user = user_to_dict(user_query)
                return auth_flow_response(user, jwt_settings)
            else:
                current_dir = getcwd()
                file_name = email.split("@")[0]
                output_file_name = path.join(current_dir, "static/avatars/") + file_name
                user = {
                    "username": name,
                    "password": None,
                    "email": email,
                    "name": name,
                    "avatar": file_name,
                    "failed_attempts": 0,
                    "lockout_time": None,
                    "type": "database",
                }
                await async_file_download(picture, output_file_name)
                saved_user = do_save_user(user, session, is_valid=True, is_oauth=True)
                user["id"] = saved_user.id
                return auth_flow_response(user, jwt_settings)
        except Exception as e:
            print(e)
            return JSONResponse({"ok": False, "ttl": "", "id": None})
