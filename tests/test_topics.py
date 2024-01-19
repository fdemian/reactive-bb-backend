import json
import pytest
from .conftest import get_test_client


@pytest.mark.asyncio
async def test_get_topics(setup_test_database):
    client = await get_test_client()

    query = """query GetTopics($limit: Int!, $offset: Int!) {
    topics(limit: $limit, offset: $offset) {
      topics {
        id
        name
        views
        replies
        created
        pinned
        closed
        user {
          id
          avatar
          username
        }
        category {
          id
          name
        }
      }
      topicsCount
    }
    }"""

    data = {
        "operationName": "GetTopics",
        "query": query.replace("\n", "").strip(),
        "variables": {"offset": 0, "limit": 5},
    }
    headers = {"content-type": "application/json"}
    response = client.post("/api/graphql", headers=headers, data=json.dumps(data))
    content = json.loads(response.content)
    topics = content["data"]["topics"]["topics"]
    topics_count = content["data"]["topics"]["topicsCount"]

    assert response.status_code == 200
    assert len(topics) == 1
    assert topics_count == 1
    assert topics[0]["id"] == 1
    assert topics[0]["name"] == "T-1000"
    assert topics[0]["views"] == 0
    assert topics[0]["pinned"] is False
    assert topics[0]["closed"] is False
    assert topics[0]["user"]["id"] == 1
    assert topics[0]["category"]["id"] == 1


@pytest.mark.asyncio
async def test_get_topic(setup_test_database):
    client = await get_test_client()

    query = """query GetTopic($id: Int!) {
     topic(id: $id) {
       id
       name
       views
       replies
       created
       pinned
       closed
       tags
       user {
         id
         avatar
         username
       }
       category {
         id
         name
       }
      }
     }"""

    data = {
        "operationName": "GetTopic",
        "query": query.replace("\n", "").strip(),
        "variables": {"id": 1},
    }
    headers = {"content-type": "application/json"}
    response = client.post("/api/graphql", headers=headers, data=json.dumps(data))
    respdata = json.loads(response.content)
    topic = respdata["data"]["topic"]

    assert response.status_code == 200

    assert topic["id"] == 1
    assert topic["name"] == "T-1000"
    assert topic["views"] == 0
    assert topic["pinned"] is False
    assert topic["closed"] is False
    assert topic["user"]["id"] == 1
    assert topic["category"]["id"] == 1


@pytest.mark.asyncio
async def test_get_topics_by_user(setup_test_database):
    client = await get_test_client()
    query = """query GetTopicsByUser($id: Int!) {
     topicsByUser(id: $id) {
       id
       name
     }
    }"""

    data = {
        "operationName": "GetTopicsByUser",
        "query": query.replace("\n", "").strip(),
        "variables": {"id": 1},
    }
    headers = {"content-type": "application/json"}
    response = client.post("/api/graphql", headers=headers, data=json.dumps(data))
    respdata = json.loads(response.content)
    topic = respdata["data"]["topicsByUser"][0]

    assert response.status_code == 200

    assert topic["id"] == 1
    assert topic["name"] == "T-1000"


@pytest.mark.asyncio
async def test_create_topics(setup_test_database):
    client = await get_test_client()
    from api.scripts.insert_test_data import user

    # Log in to the application
    login_data = json.dumps(
        {"username": user["username"], "password": user["password"]}
    )
    login_resp = client.post("/api/login", data=login_data)
    access_token = login_resp.cookies["access_token"]

    query = """query GetTopics($limit: Int!, $offset: Int!) {
    topics(limit: $limit, offset: $offset) {
      topics {
        id
        name
        views
        replies
        created
        pinned
        closed
        user {
          id
          avatar
          username
        }
        category {
          id
          name
        }
      }
      topicsCount
    }
    }"""
    data = {
        "operationName": "GetTopics",
        "query": query.replace("\n", "").strip(),
        "variables": {"offset": 0, "limit": 5},
    }
    headers = {"content-type": "application/json"}
    response = client.post("/api/graphql", headers=headers, data=json.dumps(data))
    content = json.loads(response.content)
    topics_count = content["data"]["topics"]["topicsCount"]

    assert response.status_code == 200
    assert topics_count == 1

    create_query = """
    mutation CreateTopic(
       $user: Int!
       $name: String!
       $content: String!
       $category: Int
       $tags: String
    ) {
      createTopic(
        user: $user
        name: $name
        content: $content
        category: $category
        tags: $tags
      ) {
        id
        ok
      }
    }
    """

    create_data = {
        "operationName": "CreateTopic",
        "query": create_query.replace("\n", "").strip(),
        "variables": {
            "user": 1,
            "name": "T-800",
            "content": "{}",
            "category": 1,
            "tags": "",
        },
    }

    headers = {"content-type": "application/json", "access_token": access_token}
    create_resp = client.post(
        "/api/graphql", headers=headers, data=json.dumps(create_data)
    )

    assert create_resp.status_code == 200

    create_cont = json.loads(create_resp.content)["data"]["createTopic"]

    assert create_cont["ok"] is True
    assert create_cont["id"] == 2

    verify_resp = client.post("/api/graphql", headers=headers, data=json.dumps(data))

    assert verify_resp.status_code == 200

    verify_cont = json.loads(verify_resp.content)
    verify_topics_count = verify_cont["data"]["topics"]["topicsCount"]

    assert verify_topics_count == 2


@pytest.mark.asyncio
async def test_delete_topics(setup_test_database):
    client = await get_test_client()
    from api.scripts.insert_test_data import mod_user

    # Log in to the application
    login_data = json.dumps(
        {"username": mod_user["username"], "password": mod_user["password"]}
    )
    login_resp = client.post("/api/login", data=login_data)
    access_token = login_resp.cookies["access_token"]

    query = """query GetTopics($limit: Int!, $offset: Int!) {
    topics(limit: $limit, offset: $offset) {
      topics {
        id
        name
        views
        replies
        created
        pinned
        closed
        user {
          id
          avatar
          username
        }
        category {
          id
          name
        }
      }
      topicsCount
    }
    }"""
    data = {
        "operationName": "GetTopics",
        "query": query.replace("\n", "").strip(),
        "variables": {"offset": 0, "limit": 5},
    }
    headers = {"content-type": "application/json"}
    response = client.post("/api/graphql", headers=headers, data=json.dumps(data))
    content = json.loads(response.content)
    topics_count = content["data"]["topics"]["topicsCount"]

    assert response.status_code == 200
    assert topics_count == 2

    delete_query = """
    mutation DeleteTopic($topic: Int!) {
      deleteTopic(topic: $topic)
    }
    """

    delete_data = {
        "operationName": "DeleteTopic",
        "query": delete_query.replace("\n", "").strip(),
        "variables": {"topic": 1},
    }

    headers = {"content-type": "application/json", "access_token": access_token}
    delete_resp = client.post(
        "/api/graphql", headers=headers, data=json.dumps(delete_data)
    )

    assert delete_resp.status_code == 200

    # Verify that the topic has been deleted.
    verify_resp = client.post("/api/graphql", headers=headers, data=json.dumps(data))

    assert verify_resp.status_code == 200

    verify_cont = json.loads(verify_resp.content)
    verify_topics_count = verify_cont["data"]["topics"]["topicsCount"]

    assert verify_topics_count == 1


@pytest.mark.asyncio
async def test_pin_topic_fail(setup_test_database):
    client = await get_test_client()
    from api.scripts.insert_test_data import user

    # Log in to the application
    login_data = json.dumps(
        {"username": user["username"], "password": user["password"]}
    )
    login_resp = client.post("/api/login", data=login_data)
    access_token = login_resp.cookies["access_token"]

    pin_topic_query = """mutation PinTopic($topic: Int!) {
      pinTopic(topic: $topic)
    }
    """
    pin_topic_query_data = {
        "operationName": "PinTopic",
        "query": pin_topic_query.replace("\n", "").strip(),
        "variables": {"topic": 2},
    }

    get_topic_query = """query GetTopic($id: Int!) {
       topic(id: $id) {
         id
         pinned
        }
       }
    """

    get_topic_data = {
        "operationName": "GetTopic",
        "query": get_topic_query.replace("\n", "").strip(),
        "variables": {"id": 2},
    }

    # Attempt to pin topic as an unlogged user.
    headers = {"content-type": "application/json"}
    response = client.post(
        "/api/graphql", headers=headers, data=json.dumps(pin_topic_query_data)
    )
    assert response.status_code == 200
    response = client.post(
        "/api/graphql", headers=headers, data=json.dumps(get_topic_data)
    )
    respdata = json.loads(response.content)
    topic = respdata["data"]["topic"]

    assert response.status_code == 200
    assert topic["id"] == 2
    assert topic["pinned"] is False

    # Attempt to pin topic as a regular user.
    headers = {"content-type": "application/json", "access_token": access_token}
    response = client.post(
        "/api/graphql", headers=headers, data=json.dumps(pin_topic_query_data)
    )
    assert response.status_code == 200
    response = client.post(
        "/api/graphql", headers=headers, data=json.dumps(get_topic_data)
    )
    respdata = json.loads(response.content)
    topic = respdata["data"]["topic"]

    assert response.status_code == 200
    assert topic["id"] == 2
    assert topic["pinned"] is False


@pytest.mark.asyncio
async def test_pin_unpin_topic(setup_test_database):
    client = await get_test_client()
    from api.scripts.insert_test_data import mod_user

    # Log in to the application
    login_data = json.dumps(
        {"username": mod_user["username"], "password": mod_user["password"]}
    )
    login_resp = client.post("/api/login", data=login_data)
    access_token = login_resp.cookies["access_token"]

    pin_topic_query = """mutation PinTopic($topic: Int!) {
      pinTopic(topic: $topic)
    }
    """
    pin_topic_query_data = {
        "operationName": "PinTopic",
        "query": pin_topic_query.replace("\n", "").strip(),
        "variables": {"topic": 2},
    }
    headers = {"content-type": "application/json", "access_token": access_token}
    response = client.post(
        "/api/graphql", headers=headers, data=json.dumps(pin_topic_query_data)
    )
    assert response.status_code == 200

    # Check that topic is indeed pinned.
    get_topic_query = """query GetTopic($id: Int!) {
         topic(id: $id) {
           id
           pinned
          }
         }"""

    get_topic_data = {
        "operationName": "GetTopic",
        "query": get_topic_query.replace("\n", "").strip(),
        "variables": {"id": 2},
    }
    response = client.post(
        "/api/graphql", headers=headers, data=json.dumps(get_topic_data)
    )
    respdata = json.loads(response.content)
    topic = respdata["data"]["topic"]

    assert response.status_code == 200
    assert topic["id"] == 2
    assert topic["pinned"] is True

    # Unpin topic
    response = client.post(
        "/api/graphql", headers=headers, data=json.dumps(pin_topic_query_data)
    )
    assert response.status_code == 200

    response = client.post(
        "/api/graphql", headers=headers, data=json.dumps(get_topic_data)
    )
    respdata = json.loads(response.content)
    topic = respdata["data"]["topic"]

    assert response.status_code == 200
    assert topic["id"] == 2
    assert topic["pinned"] is False


# Verify that an unlogged or regular user  cannot delete topics.
@pytest.mark.asyncio
async def test_delete_topics_fail(setup_test_database):
    client = await get_test_client()
    from api.scripts.insert_test_data import user

    # Log in to the application with a regular user.
    login_data = json.dumps(
        {"username": user["username"], "password": user["password"]}
    )
    login_resp = client.post("/api/login", data=login_data)
    access_token = login_resp.cookies["access_token"]

    query = """query GetTopics($limit: Int!, $offset: Int!) {
    topics(limit: $limit, offset: $offset) {
      topics {
        id
        name
        views
        replies
        created
        pinned
        closed
        user {
          id
          avatar
          username
        }
        category {
          id
          name
        }
      }
      topicsCount
    }
    }"""
    data = {
        "operationName": "GetTopics",
        "query": query.replace("\n", "").strip(),
        "variables": {"offset": 0, "limit": 5},
    }
    headers = {"content-type": "application/json"}
    response = client.post("/api/graphql", headers=headers, data=json.dumps(data))
    content = json.loads(response.content)
    topics_count = content["data"]["topics"]["topicsCount"]

    assert response.status_code == 200
    assert topics_count == 1

    delete_query = """
    mutation DeleteTopic($topic: Int!) {
      deleteTopic(topic: $topic)
    }
    """
    delete_data = {
        "operationName": "DeleteTopic",
        "query": delete_query.replace("\n", "").strip(),
        "variables": {"topic": 1},
    }

    # Verify deletion for unlogged users
    headers = {"content-type": "application/json"}
    delete_resp = client.post(
        "/api/graphql", headers=headers, data=json.dumps(delete_data)
    )
    assert delete_resp.status_code == 200
    delete_fail_cont = json.loads(delete_resp.content)
    assert delete_fail_cont["data"] is None
    assert delete_fail_cont["errors"][0]["message"] == "Invalid auth credentials"
    # Verify that the topic has not been deleted.
    verify_resp = client.post("/api/graphql", headers=headers, data=json.dumps(data))
    assert verify_resp.status_code == 200
    verify_cont = json.loads(verify_resp.content)
    verify_topics_count = verify_cont["data"]["topics"]["topicsCount"]
    assert verify_topics_count == 1

    # Verify that a regular user cannot delete the topic as well.
    headers = {"content-type": "application/json", "access_token": access_token}
    delete_resp = client.post(
        "/api/graphql", headers=headers, data=json.dumps(delete_data)
    )
    assert delete_resp.status_code == 200
    delete_fail_cont = json.loads(delete_resp.content)
    assert delete_fail_cont["data"] is None
    assert delete_fail_cont["errors"][0]["message"] == "Invalid permissions"

    # Verify that the topic has not been deleted.
    verify_resp = client.post("/api/graphql", headers=headers, data=json.dumps(data))
    assert verify_resp.status_code == 200

    verify_cont = json.loads(verify_resp.content)
    verify_topics_count = verify_cont["data"]["topics"]["topicsCount"]
    assert verify_topics_count == 1


@pytest.mark.asyncio
async def test_close_and_reopen_topic(setup_test_database):
    client = await get_test_client()
    from api.scripts.insert_test_data import mod_user

    # Log in to the application
    login_data = json.dumps(
        {"username": mod_user["username"], "password": mod_user["password"]}
    )
    login_resp = client.post("/api/login", data=login_data)
    access_token = login_resp.cookies["access_token"]

    query = """query GetTopic($id: Int!) {
     topic(id: $id) {
       id
       name
       views
       replies
       created
       pinned
       closed
       tags
       user {
         id
         avatar
         username
       }
       category {
         id
         name
       }
      }
     }"""

    data = {
        "operationName": "GetTopic",
        "query": query.replace("\n", "").strip(),
        "variables": {"id": 1},
    }
    headers = {"content-type": "application/json"}
    response = client.post("/api/graphql", headers=headers, data=json.dumps(data))
    respdata = json.loads(response.content)
    topic = respdata["data"]["topic"]

    assert response.status_code == 200
    assert topic["id"] == 1
    assert topic["closed"] is False

    close_query = """
    mutation CloseTopic($topic: Int!) {
      closeTopic(topic: $topic)
    }
    """
    close_data = {
        "operationName": "CloseTopic",
        "query": close_query.replace("\n", "").strip(),
        "variables": {"topic": 1},
    }
    auth_headers = {"content-type": "application/json", "access_token": access_token}
    close_resp = client.post(
        "/api/graphql", headers=auth_headers, data=json.dumps(close_data)
    )

    assert close_resp.status_code == 200

    # Verify that topic is closed.
    response_2 = client.post("/api/graphql", headers=headers, data=json.dumps(data))
    resp_data_2 = json.loads(response_2.content)
    topic_c = resp_data_2["data"]["topic"]

    assert response_2.status_code == 200
    assert topic_c["id"] == 1
    assert topic_c["closed"] is True

    # Reopen the topic.
    reopen_query = """
    mutation ReopenTopic($topic: Int!) {
      reopenTopic(topic: $topic)
    }
    """
    reopen_data = {
        "operationName": "ReopenTopic",
        "query": reopen_query.replace("\n", "").strip(),
        "variables": {"topic": 1},
    }
    auth_headers = {"content-type": "application/json", "access_token": access_token}
    reopen_resp = client.post(
        "/api/graphql", headers=auth_headers, data=json.dumps(reopen_data)
    )
    assert reopen_resp.status_code == 200

    # Verify that has effectively been reopened
    response_3 = client.post("/api/graphql", headers=headers, data=json.dumps(data))
    resp_data_3 = json.loads(response_3.content)
    topic_r = resp_data_3["data"]["topic"]

    assert response_3.status_code == 200
    assert topic_r["id"] == 1
    assert topic_r["closed"] is False


@pytest.mark.asyncio
async def test_increase_topic_views(setup_test_database):
    client = await get_test_client()
    from api.scripts.insert_test_data import user

    # Log in to the application
    login_data = json.dumps(
        {"username": user["username"], "password": user["password"]}
    )
    login_resp = client.post("/api/login", data=login_data)
    access_token = login_resp.cookies["access_token"]

    query = """query GetTopic($id: Int!) {
     topic(id: $id) {
       id
       name
       views
       replies
       created
       pinned
       closed
       tags
       user {
         id
         avatar
         username
       }
       category {
         id
         name
       }
      }
     }"""

    data = {
        "operationName": "GetTopic",
        "query": query.replace("\n", "").strip(),
        "variables": {"id": 2},
    }
    headers = {"content-type": "application/json"}
    response = client.post("/api/graphql", headers=headers, data=json.dumps(data))
    respdata = json.loads(response.content)
    topic = respdata["data"]["topic"]

    assert response.status_code == 200

    print(respdata)
    print(">>>>>>>>>>>>>>>>>>>>>>")
    assert topic["views"] == 0

    # Increase views
    iv_headers = {"content-type": "application/json", "access_token": access_token}

    iv_query = """mutation IncreaseViewCount($topic: Int!) {
      increaseViewCount(topic: $topic) {
        id
        ok
      }
    }"""

    iv_data = {
        "operationName": "IncreaseViewCount",
        "query": iv_query.replace("\n", "").strip(),
        "variables": {"topic": 2},
    }
    iv_resp = client.post("/api/graphql", headers=iv_headers, data=json.dumps(iv_data))
    iv_cont = json.loads(iv_resp.content)["data"]["increaseViewCount"]

    assert iv_cont["ok"] is True
    assert iv_cont["id"] == 2

    # Check that the topic views have increased.
    response_2 = client.post("/api/graphql", headers=headers, data=json.dumps(data))
    topic_2 = json.loads(response_2.content)["data"]["topic"]

    assert response_2.status_code == 200
    assert topic_2["views"] == 1
