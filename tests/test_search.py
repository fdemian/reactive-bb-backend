import json
import pytest
from .conftest import get_test_client


@pytest.mark.asyncio
async def test_search_posts(setup_test_database):
    client = await get_test_client()

    from api.scripts.insertdata.insert_user import user

    # Log in to the application
    login_data = json.dumps(
        {"username": user["username"], "password": user["password"]}
    )
    login_resp = client.post("/api/login", data=login_data)
    access_token = login_resp.cookies["access_token"]

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

    for post in posts:
        assert "Post#" in post["text"]


@pytest.mark.asyncio
async def test_search_topics(setup_test_database):
    client = await get_test_client()

    from api.scripts.insertdata.insert_user import user

    # Log in to the application
    login_data = json.dumps(
        {"username": user["username"], "password": user["password"]}
    )
    login_resp = client.post("/api/login", data=login_data)
    access_token = login_resp.cookies["access_token"]

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
        "variables": {"term": "T-1000", "where": ["titles"], "offset": 0, "limit": 5},
    }

    headers = {"content-type": "application/json", "access_token": access_token}

    response = client.post("/api/graphql", headers=headers, data=json.dumps(data))
    respdata = json.loads(response.content)

    search_results = respdata["data"]["search"]
    topics = search_results["results"]
    total = search_results["total"]

    assert response.status_code == 200
    assert total == 1
    assert len(topics) == 1
    assert topics[0]["topicId"] == 1
    assert topics[0]["topic"] == "T-1000"


@pytest.mark.asyncio
async def test_search_topics_title_post(setup_test_database):
    client = await get_test_client()

    from api.scripts.insertdata.insert_user import user

    # Log in to the application
    login_data = json.dumps(
        {"username": user["username"], "password": user["password"]}
    )
    login_resp = client.post("/api/login", data=login_data)
    access_token = login_resp.cookies["access_token"]

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
        "variables": {
            "term": "T-1000",
            "where": ["titles", "posts"],
            "offset": 0,
            "limit": 5,
        },
    }

    headers = {"content-type": "application/json", "access_token": access_token}

    response = client.post("/api/graphql", headers=headers, data=json.dumps(data))
    respdata = json.loads(response.content)

    search_results = respdata["data"]["search"]
    results = search_results["results"]
    total = search_results["total"]

    assert response.status_code == 200
    assert total == 1001
    assert len(results) == 1
    assert results[0]["topicId"] == 1
    assert results[0]["topic"] == "T-1000"
