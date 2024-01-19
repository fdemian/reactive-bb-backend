import json
import pytest
from datetime import datetime, timedelta
from .conftest import get_test_client


@pytest.mark.asyncio
async def test_ban_users_correctly(setup_test_database):
    client = await get_test_client()
    from api.scripts.insert_test_data import mod_user

    # Get credentials.
    data = json.dumps(
        {"username": mod_user["username"], "password": mod_user["password"]}
    )
    login_resp = client.post("/api/login", data=data)
    access_token = login_resp.cookies["access_token"]

    # Check that the user is not banned.
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
        "variables": {"id": 2},
    }

    headers = {"content-type": "application/json", "access_token": access_token}
    response = client.post("/api/graphql", headers=headers, data=json.dumps(data))
    content = json.loads(response.content)
    user_data = content["data"]["getUser"]

    assert user_data["banned"] is False

    ban_reason = '{"root":{"children":[{"children":[{"detail":0,"format":0,"mode":"normal","style":"","text":"BAN_REASON","type":"text","version":1}],"direction":"ltr","format":"","indent"'
    ban_expires = datetime.today() + timedelta(days=7)

    # Ban user
    ban_query = """
    mutation BanUser($user: Int!, $expires: Datetime!, $reason: String!) {
      banUser(user: $user, expires: $expires, reason: $reason)
    }
    """
    ban_data = {
        "operationName": "BanUser",
        "query": ban_query.replace("\n", "").strip(),
        "variables": {
            "user": 2,
            "expires": ban_expires.isoformat(),
            "reason": ban_reason,
        },
    }

    ban_resp = client.post("/api/graphql", headers=headers, data=json.dumps(ban_data))
    ban_data = json.loads(ban_resp.content)["data"]["banUser"]
    assert ban_data is True

    # Check that user is banned.
    banned_resp = client.post("/api/graphql", headers=headers, data=json.dumps(data))
    banned_cont = json.loads(banned_resp.content)
    banned_user = banned_cont["data"]["getUser"]

    assert banned_user["banned"] is True
    assert banned_user["banReason"] == ban_reason

    # Remove user ban.
    remove_ban_query = """
    mutation RemoveUserBan($user: Int!) {
      removeUserBan(user: $user)
    }
    """
    remove_ban_data = {
        "operationName": "RemoveUserBan",
        "query": remove_ban_query.replace("\n", "").strip(),
        "variables": {"user": 2},
    }

    remove_ban_resp = client.post(
        "/api/graphql", headers=headers, data=json.dumps(remove_ban_data)
    )
    remove_ban_data = json.loads(remove_ban_resp.content)["data"]["removeUserBan"]
    assert remove_ban_data is True

    # Check that user is not banned.
    not_banned_resp = client.post(
        "/api/graphql", headers=headers, data=json.dumps(data)
    )
    not_banned_cont = json.loads(not_banned_resp.content)
    not_banned_user = not_banned_cont["data"]["getUser"]

    assert not_banned_user["banned"] is False
    assert not_banned_user["banReason"] is None


@pytest.mark.asyncio
async def test_ban_without_permissions(setup_test_database):
    client = await get_test_client()
    from api.scripts.insert_test_data import user

    # Get credentials.
    data = json.dumps({"username": user["username"], "password": user["password"]})
    login_resp = client.post("/api/login", data=data)
    access_token = login_resp.cookies["access_token"]

    # Check that the user is not banned.
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
        "variables": {"id": 2},
    }

    headers = {"content-type": "application/json", "access_token": access_token}
    response = client.post("/api/graphql", headers=headers, data=json.dumps(data))
    content = json.loads(response.content)
    user_data = content["data"]["getUser"]

    assert user_data["banned"] is False

    ban_reason = "BAN REASON"
    ban_expires = datetime.today() + timedelta(days=7)

    # Ban user
    ban_query = """
    mutation BanUser($user: Int!, $expires: Datetime!, $reason: String!) {
      banUser(user: $user, expires: $expires, reason: $reason)
    }
    """
    ban_data = {
        "operationName": "BanUser",
        "query": ban_query.replace("\n", "").strip(),
        "variables": {
            "user": 2,
            "expires": ban_expires.isoformat(),
            "reason": ban_reason,
        },
    }
    ban_resp = client.post("/api/graphql", headers=headers, data=json.dumps(ban_data))
    ban_data = json.loads(ban_resp.content)["data"]["banUser"]

    assert ban_data is None

    # Check that user is not banned.
    banned_resp = client.post("/api/graphql", headers=headers, data=json.dumps(data))
    banned_cont = json.loads(banned_resp.content)
    banned_user = banned_cont["data"]["getUser"]

    assert banned_user["banned"] is False
    assert banned_user["banReason"] is None


@pytest.mark.asyncio
async def test_remove_ban_without_permissions(setup_test_database):
    client = await get_test_client()
    from api.scripts.insert_test_data import user

    # Get credentials.
    data = json.dumps({"username": user["username"], "password": user["password"]})
    login_resp = client.post("/api/login", data=data)
    access_token = login_resp.cookies["access_token"]

    # Check that the user is not banned.
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
        "variables": {"id": 5},
    }

    headers = {"content-type": "application/json", "access_token": access_token}
    response = client.post("/api/graphql", headers=headers, data=json.dumps(data))
    content = json.loads(response.content)
    user_data = content["data"]["getUser"]

    assert user_data["banned"] is True

    # Remove user ban.
    remove_ban_query = """
        mutation RemoveUserBan($user: Int!) {
          removeUserBan(user: $user)
        }
        """
    remove_ban_data = {
        "operationName": "RemoveUserBan",
        "query": remove_ban_query.replace("\n", "").strip(),
        "variables": {"user": 5},
    }

    remove_ban_resp = client.post(
        "/api/graphql", headers=headers, data=json.dumps(remove_ban_data)
    )
    remove_ban_data = json.loads(remove_ban_resp.content)["data"]["removeUserBan"]
    assert remove_ban_data is None
