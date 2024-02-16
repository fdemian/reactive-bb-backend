import json
import pytest
from .conftest import get_test_client


@pytest.mark.asyncio
async def test_get_user(setup_test_database):
    client = await get_test_client()

    query = """query GetUser($id: Int!) {
        getUser(id: $id) {
          id
          username
          avatar
          fullname
          email
          status
          about
          banned
          banReason
        }
    }"""

    data = {
        "operationName": "GetUser",
        "query": query.replace("\n", "").strip(),
        "variables": {"id": 1},
    }
    headers = {"content-type": "application/json"}
    response = client.post("/api/graphql", headers=headers, data=json.dumps(data))
    content = json.loads(response.content)
    user_cont = content["data"]["getUser"]

    assert response.status_code == 200
    assert user_cont["id"] == 1
    assert user_cont["username"] == "user"
    assert user_cont["fullname"] == "name"

    assert user_cont["avatar"] is None
    assert user_cont["email"] == "user@email.com"
    assert user_cont["status"] is None
    assert user_cont["about"] is None
    assert user_cont["banned"] is False
    assert user_cont["banReason"] is None


@pytest.mark.asyncio
async def test_validate_user_nexists(setup_test_database):
    client = await get_test_client()

    query = """query CheckUsername($username: String!) {
      checkUsername(username: $username) {
        exists
      }
    }"""
    headers = {"content-type": "application/json"}

    # Verify that an existing user exists.
    data = {
        "operationName": "CheckUsername",
        "query": query.replace("\n", "").strip(),
        "variables": {"username": "user"},
    }

    existing_user_resp = client.post(
        "/api/graphql", headers=headers, data=json.dumps(data)
    )
    assert existing_user_resp.status_code == 200

    content = json.loads(existing_user_resp.content)["data"]["checkUsername"]

    assert content["exists"] is True

    # Verify a nonexistent username.
    data = {
        "operationName": "CheckUsername",
        "query": query.replace("\n", "").strip(),
        "variables": {"username": "nonexistentuser"},
    }
    non_exist_user_resp = client.post(
        "/api/graphql", headers=headers, data=json.dumps(data)
    )
    assert non_exist_user_resp.status_code == 200
    content_2 = json.loads(non_exist_user_resp.content)["data"]["checkUsername"]
    assert content_2["exists"] is False


@pytest.mark.asyncio
async def test_validate_user(setup_test_database):
    client = await get_test_client()
    from .helpers import get_activation_token

    # Create new user

    test_user = {
        "username": "userTest",
        "password": "userPass",
        "email": "user_test@email.com",
    }

    query = """mutation CreateUser($username: String!, $password: String!, $email: String!) {
        createUser(username: $username, password: $password, email: $email) {
          ok
          id
          message
          email
        }
    }"""
    headers = {"content-type": "application/json"}
    data = {
        "operationName": "CreateUser",
        "query": query.replace("\n", "").strip(),
        "variables": {
            "username": test_user["username"],
            "password": test_user["password"],
            "email": test_user["email"],
        },
    }
    create_resp = client.post("/api/graphql", headers=headers, data=json.dumps(data))

    assert create_resp.status_code == 200

    create_cont = json.loads(create_resp.content)["data"]["createUser"]

    assert create_cont["ok"] is True
    assert create_cont["email"] == test_user["email"]

    created_id = create_cont["id"]

    token = get_activation_token(create_cont["email"])

    # Verify that the newly created user can't log in.
    bad_login_data = json.dumps(
        {"username": test_user["username"], "password": test_user["password"]}
    )
    bad_login_resp = client.post("/api/login", data=bad_login_data)
    bad_login_cont = json.loads(bad_login_resp.content)

    assert bad_login_cont["ok"] is False
    assert bad_login_cont["id"] is None

    # Validate user

    validate_query = """
    mutation ValidateUser($token: String!) {
      validateUser(token: $token) {
        id
        ok
      }
    }
    """
    validate_data = {
        "operationName": "ValidateUser",
        "query": validate_query.replace("\n", "").strip(),
        "variables": {"token": token},
    }
    validate_resp = client.post(
        "/api/graphql", headers=headers, data=json.dumps(validate_data)
    )

    assert validate_resp.status_code == 200

    validate_cont = json.loads(validate_resp.content)["data"]["validateUser"]

    assert validate_cont["ok"] is True
    assert validate_cont["id"] == created_id

    # Verify that the user can log in now that it is activated.
    login_data = json.dumps(
        {"username": test_user["username"], "password": test_user["password"]}
    )
    login_resp = client.post("/api/login", data=login_data)

    assert login_resp.status_code == 200

    login_cont = json.loads(login_resp.content)

    access_token = login_resp.cookies["access_token"]
    refresh_token = login_resp.cookies["refresh_token"]

    assert login_cont["ok"] is True
    assert access_token is not None
    assert refresh_token is not None


@pytest.mark.asyncio
async def test_update_email(setup_test_database):
    client = await get_test_client()
    from api.scripts.insert_test_data import user

    # Get login credentials
    login_data = json.dumps(
        {"username": user["username"], "password": user["password"]}
    )
    login_resp = client.post("/api/login", data=login_data)
    access_token = login_resp.cookies["access_token"]

    headers = {"content-type": "application/json", "access_token": access_token}

    query = """query GetUser($id: Int!) {
        getUser(id: $id) {
          id
          username
          avatar
          fullname
          email
          status
          about
        }
     }"""

    data = {
        "operationName": "GetUser",
        "query": query.replace("\n", "").strip(),
        "variables": {"id": 1},
    }

    response = client.post("/api/graphql", headers=headers, data=json.dumps(data))
    user_resp_data = json.loads(response.text)["data"]["getUser"]

    new_email = "fake_mail@user.com"
    assert user_resp_data["email"] == user["email"]
    assert user_resp_data["email"] is not new_email

    # Change the user's email.
    update_email_query = """mutation UpdateEmail($id: Int!, $email: String!) {
        updateEmail(id: $id, email: $email)
     }"""

    update_email_data = {
        "operationName": "UpdateEmail",
        "query": update_email_query.replace("\n", "").strip(),
        "variables": {"id": user_resp_data["id"], "email": new_email},
    }
    email_resp = client.post(
        "/api/graphql", headers=headers, data=json.dumps(update_email_data)
    )

    assert email_resp.status_code == 200

    # Verify that the email has changed.
    verify_resp = client.post("/api/graphql", headers=headers, data=json.dumps(data))
    verify_resp_data = json.loads(verify_resp.text)["data"]["getUser"]

    assert verify_resp_data["email"] is not user["email"]
    assert verify_resp_data["email"] == new_email


@pytest.mark.asyncio
async def test_update_profile_data(setup_test_database):
    client = await get_test_client()
    from api.scripts.insert_test_data import user

    # Get login credentials
    login_data = json.dumps(
        {"username": user["username"], "password": user["password"]}
    )
    login_resp = client.post("/api/login", data=login_data)
    access_token = login_resp.cookies["access_token"]

    headers = {"content-type": "application/json", "access_token": access_token}

    query = """query GetUser($id: Int!) {
        getUser(id: $id) {
          id
          status
          about
        }
     }"""

    data = {
        "operationName": "GetUser",
        "query": query.replace("\n", "").strip(),
        "variables": {"id": 1},
    }

    response = client.post("/api/graphql", headers=headers, data=json.dumps(data))
    user_resp_data = json.loads(response.text)["data"]["getUser"]

    new_status = "A NEW STATUS"
    new_about_text = "A NEW ABOUT TEXT"

    assert user_resp_data["status"] is None
    assert user_resp_data["about"] is None
    assert user_resp_data["status"] is not new_status
    assert user_resp_data["about"] is not new_about_text

    # Change the user's email.
    update_profile_query = """  mutation UpdateProfile($id: Int!, $status:String, $about:String) {
    updateProfile(id:$id, status:$status, about:$about) {
      ok
    }
        }"""

    update_profile_data = {
        "operationName": "UpdateProfile",
        "query": update_profile_query.replace("\n", "").strip(),
        "variables": {
            "id": user_resp_data["id"],
            "status": new_status,
            "about": new_about_text,
        },
    }
    update_prof_resp = client.post(
        "/api/graphql", headers=headers, data=json.dumps(update_profile_data)
    )
    assert update_prof_resp.status_code == 200

    # Verify that the email has changed.
    update_verify = client.post("/api/graphql", headers=headers, data=json.dumps(data))
    update_verify_data = json.loads(update_verify.text)["data"]["getUser"]

    assert update_verify_data["status"] is not user["status"]
    assert update_verify_data["status"] == new_status

    assert update_verify_data["about"] is not user["about"]
    assert update_verify_data["about"] == new_about_text


@pytest.mark.asyncio
async def test_update_password(setup_test_database):
    client = await get_test_client()
    from api.scripts.insert_test_data import user

    # Get login credentials
    login_data = json.dumps(
        {"username": user["username"], "password": user["password"]}
    )
    login_resp = client.post("/api/login", data=login_data)
    access_token = login_resp.cookies["access_token"]

    headers = {"content-type": "application/json", "access_token": access_token}

    # Verify that new password does not work
    new_pass = "newpass"
    fail_login_data = json.dumps({"username": user["username"], "password": new_pass})
    fail_login_resp = client.post("/api/login", data=fail_login_data)
    fail_login_cont = json.loads(fail_login_resp.text)

    assert fail_login_cont["ok"] is False
    assert fail_login_cont["id"] is None
    assert fail_login_cont["ttl"] == ""

    update_pass_query = """
       mutation UpdatePassword($id: Int!, $currentPass: String!, $newPass: String!) {
         updatePassword(id: $id, currentPass: $currentPass, newPass: $newPass) {
          ok
         }
       }
      """

    update_pass_data = {
        "operationName": "UpdatePassword",
        "query": update_pass_query.replace("\n", "").strip(),
        "variables": {"id": 1, "currentPass": user["password"], "newPass": new_pass},
    }

    update_resp = client.post(
        "/api/graphql", headers=headers, data=json.dumps(update_pass_data)
    )
    assert update_resp.status_code == 200

    update_resp_cont = json.loads(update_resp.text)["data"]
    assert update_resp_cont["updatePassword"]["ok"] is True

    # Verify that it is not possible for the user to log in with the old password
    bad_login_resp = client.post("/api/login", data=login_data)
    bad_login_cont = json.loads(bad_login_resp.text)

    assert bad_login_cont["ok"] is False
    assert bad_login_cont["id"] is None
    assert bad_login_cont["ttl"] == ""

    # Verify that it is possible to log in with the new password
    new_login_data = json.dumps({"username": user["username"], "password": new_pass})
    new_login_resp = client.post("/api/login", data=new_login_data)
    new_login_cont = json.loads(new_login_resp.text)

    assert new_login_cont["ok"] is True
    assert new_login_cont["id"] is not None
    assert new_login_cont["ttl"] != ""
