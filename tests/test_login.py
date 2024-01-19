import json
import pytest
import time
from .conftest import get_test_client


@pytest.mark.asyncio
async def test_login_and_logout(setup_test_database):
    client = await get_test_client()
    from api.scripts.insert_test_data import user

    data = json.dumps({"username": user["username"], "password": user["password"]})
    login_resp = client.post("/api/login", data=data)
    login_cont = json.loads(login_resp.content)

    access_token = login_resp.cookies["access_token"]
    refresh_token = login_resp.cookies["refresh_token"]

    assert login_resp.status_code == 200
    assert login_cont["id"] == 1
    assert login_cont["ok"] is True

    assert access_token is not None
    assert refresh_token is not None

    logout_resp = client.post("/api/logout")
    logout_cont = json.loads(logout_resp.content)

    assert logout_resp.status_code == 200
    assert logout_cont["ok"] is True
    assert len(logout_resp.cookies) == 0
    assert "set-cookie" in logout_resp.headers


@pytest.mark.asyncio
async def test_wrong_password(setup_test_database):
    client = await get_test_client()
    from api.scripts.insert_test_data import user

    data = json.dumps(
        {"username": user["username"], "password": user["password"] + "__WRONG"}
    )
    login_wp_resp = client.post("/api/login", data=data)
    login_wp_cont = json.loads(login_wp_resp.content)

    assert login_wp_resp.status_code == 200
    assert login_wp_cont["id"] is None
    assert login_wp_cont["ok"] is False


@pytest.mark.asyncio
async def test_wrong_user(setup_test_database):
    client = await get_test_client()
    from api.scripts.insert_test_data import user

    data = json.dumps(
        {"username": user["username"] + "____WRONG", "password": user["password"]}
    )
    login_wp_resp = client.post("/api/login", data=data)
    login_wp_cont = json.loads(login_wp_resp.content)

    assert login_wp_resp.status_code == 200
    assert login_wp_cont["id"] is None
    assert login_wp_cont["ok"] is False


@pytest.mark.asyncio
async def test_lock_user(setup_test_database):
    client = await get_test_client()
    from api.scripts.insert_test_data import user

    # Exhaust the number of login tries with wrong passwords.
    for i in range(4):
        data = json.dumps(
            {"username": user["username"], "password": user["password"] + "__WRONG"}
        )

        login_wp_resp = client.post("/api/login", data=data)
        login_wp_cont = json.loads(login_wp_resp.content)

        #
        assert login_wp_resp.status_code == 200
        assert login_wp_cont["id"] is None
        assert login_wp_cont["ok"] is False

    # Try to login.
    data = json.dumps({"username": user["username"], "password": user["password"]})
    login_wp_resp = client.post("/api/login", data=data)
    login_wp_cont = json.loads(login_wp_resp.content)
    assert login_wp_resp.status_code == 200
    assert login_wp_cont["id"] is None
    assert login_wp_cont["ok"] is False


@pytest.mark.asyncio
async def test_auth_expired(setup_test_database):
    client = await get_test_client()
    from api.scripts.insert_test_data import user

    data = json.dumps({"username": user["username"], "password": user["password"]})
    login_resp = client.post("/api/login", data=data)
    login_cont = json.loads(login_resp.content)
    access_token = login_resp.cookies["access_token"]
    refresh_token = login_resp.cookies["refresh_token"]
    ttl = login_cont["ttl"]

    assert login_resp.status_code == 200
    assert login_cont["id"] == 1
    assert login_cont["ok"] is True

    assert access_token is not None
    assert refresh_token is not None

    query = """query GetSearch($term: String!, $where: [String!], $limit: Int!, $offset: Int!) {
      search(term: $term, where: $where, limit: $limit, offset: $offset) {
        results {
          id
          text
          topicId
          topic
        }
        total
        }
    }"""

    data = {
        "operationName": "GetSearch",
        "query": query.replace("\n", "").strip(),
        "variables": {"term": "Post", "where": ["posts"], "offset": 0, "limit": 5},
    }

    search_headers = {"content-type": "application/json", "access_token": access_token}

    response = client.post(
        "/api/graphql", headers=search_headers, data=json.dumps(data)
    )
    respdata = json.loads(response.content)

    search_results = respdata["data"]["search"]
    posts = search_results["results"]
    total = search_results["total"]

    assert response.status_code == 200
    assert total == 1000
    assert len(posts) == 5

    # Wait until the token expires.
    sleep_time = float(int(ttl) / 1000)
    time.sleep(sleep_time)
    #

    response = client.post(
        "/api/graphql", headers=search_headers, data=json.dumps(data)
    )
    assert response.status_code == 412


@pytest.mark.asyncio
async def test_refresh(setup_test_database):
    client = await get_test_client()
    from api.scripts.insert_test_data import user

    data = json.dumps({"username": user["username"], "password": user["password"]})
    login_resp = client.post("/api/login", data=data)
    login_cont = json.loads(login_resp.text)

    access_token = login_resp.cookies["refresh_token"]
    refresh_token = login_resp.cookies["refresh_token"]

    assert login_resp.status_code == 200
    assert login_cont["id"] == 1
    assert login_cont["ok"] is True
    assert refresh_token is not None

    refresh_headers = {
        "content-type": "application/json",
        "access_token": access_token,
        "refresh_token": refresh_token,
    }

    refresh_resp = client.post("/api/refresh", headers=refresh_headers)
    refresh_cont = json.loads(refresh_resp.text)

    assert refresh_resp.status_code == 200
    assert refresh_cont["ok"] is True
    assert refresh_resp.cookies["access_token"] is not None
    assert refresh_resp.cookies["refresh_token"] is not None
