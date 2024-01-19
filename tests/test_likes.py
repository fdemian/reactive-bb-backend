import json
import pytest
from .conftest import get_test_client


@pytest.mark.asyncio
async def test_add_and_remove_likes(setup_test_database):
    client = await get_test_client()
    from api.scripts.insert_test_data import user

    # Log in to the application
    login_data = json.dumps(
        {"username": user["username"], "password": user["password"]}
    )
    login_resp = client.post("/api/login", data=login_data)
    access_token = login_resp.cookies["access_token"]

    query = """query GetLikesByUser($id: Int!) {
      likesByUser(id: $id) {
        id
        post {
          id
          topicId
          content
        }
      }
    }"""
    data = {
        "operationName": "GetLikesByUser",
        "query": query.replace("\n", "").strip(),
        "variables": {"id": 1},
    }
    headers = {"content-type": "application/json"}
    response = client.post("/api/graphql", headers=headers, data=json.dumps(data))
    respdata = json.loads(response.content)
    likes = respdata["data"]["likesByUser"]

    assert response.status_code == 200
    assert len(likes) == 0

    query_mut = """mutation LikePost($user: Int!, $originator: Int!, $topic: Int!, $post: Int!) {
        likePost(user: $user, originator: $originator, topic: $topic, post: $post) {
          id
          ok
          postId
          likes
        }
      } 
    """
    data_mut = {
        "operationName": "LikePost",
        "query": query_mut.replace("\n", "").strip(),
        "variables": {"user": 1, "originator": 1, "topic": 1, "post": 1},
    }
    headers_mut = {"content-type": "application/json", "access_token": access_token}
    response_mut = client.post(
        "/api/graphql", headers=headers_mut, data=json.dumps(data_mut)
    )
    mut_cont = json.loads(response_mut.content)
    mut_data = mut_cont["data"]["likePost"]

    assert response_mut.status_code == 200
    assert mut_data["ok"] is True
    assert mut_data["id"] == 1
    assert mut_data["postId"] == 1

    # Query for likes again.
    likes_resp = client.post("/api/graphql", headers=headers, data=json.dumps(data))
    new_resp_data = json.loads(likes_resp.content)
    likes = new_resp_data["data"]["likesByUser"]

    assert likes_resp.status_code == 200
    assert len(likes) == 1
    assert likes[0]["id"] == 1
    assert likes[0]["post"]["id"] == 1
    assert likes[0]["post"]["topicId"] == 1
    assert likes[0]["post"]["content"] is not None

    # Remove like from post.
    remove_mut = """mutation RemoveLike($user: Int!, $post: Int!) {
        removeLike(user: $user, post: $post) {
          id
          ok
          postId
          likes
        }
     }
    """
    remove_data = {
        "operationName": "RemoveLike",
        "query": remove_mut.replace("\n", "").strip(),
        "variables": {"user": 1, "post": 1},
    }
    headers_remove = {"content-type": "application/json", "access_token": access_token}
    remove_mut = client.post(
        "/api/graphql", headers=headers_remove, data=json.dumps(remove_data)
    )

    assert remove_mut.status_code == 200

    # Query for likes again.
    likes_resp_rem = client.post("/api/graphql", headers=headers, data=json.dumps(data))
    removed_resp_data = json.loads(likes_resp_rem.content)
    current_likes = removed_resp_data["data"]["likesByUser"]

    assert likes_resp.status_code == 200
    assert len(current_likes) == 0
