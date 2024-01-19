import json
import pytest
from .conftest import get_test_client


@pytest.mark.asyncio
async def test_flag_unflag_post(setup_test_database):
    client = await get_test_client()
    from api.scripts.insert_test_data import user

    # Get credentials.
    data = json.dumps({"username": user["username"], "password": user["password"]})
    login_resp = client.post("/api/login", data=data)
    access_token = login_resp.cookies["access_token"]

    # There are no flagged posts
    flag_query = """
    query GetFlaggedPosts($offset: Int!, $limit: Int!) {
        flaggedPosts(offset: $offset, limit: $limit) {
          postId
          userId
          reasonId
          reasonText
        }
    }
    """
    flag_q_data = {
        "operationName": "GetFlaggedPosts",
        "query": flag_query.replace("\n", "").strip(),
        "variables": {"limit": 5, "offset": 0},
    }
    headers = {"content-type": "application/json", "access_token": access_token}
    response = client.post(
        "/api/graphql", headers=headers, data=json.dumps(flag_q_data)
    )
    respdata = json.loads(response.content)["data"]["flaggedPosts"]

    assert len(respdata) == 0

    flag_reason_text = "Flag Reason"

    # Flag post
    add_flag_query = """
    mutation FlagPost($post: Int!, $user: Int!, $reason: Int!, $text: String) {
      flagPost(post: $post, user: $user, reason: $reason, text: $text)
    }
    """
    add_flag_data = {
        "operationName": "FlagPost",
        "query": add_flag_query.replace("\n", "").strip(),
        "variables": {"post": 5, "user": 1, "reason": 4, "text": flag_reason_text},
    }
    flag_resp = client.post(
        "/api/graphql", headers=headers, data=json.dumps(add_flag_data)
    )

    assert flag_resp.status_code == 200
    flag_cont = json.loads(flag_resp.content)["data"]["flagPost"]
    assert flag_cont is True

    # Verify that post has been flagged.
    verify_f_resp = client.post(
        "/api/graphql", headers=headers, data=json.dumps(flag_q_data)
    )
    verify_f_data = json.loads(verify_f_resp.content)["data"]["flaggedPosts"]

    assert len(verify_f_data) == 1
    assert verify_f_data[0]["userId"] == 1
    assert verify_f_data[0]["postId"] == 5
    assert verify_f_data[0]["reasonId"] == 4
    assert verify_f_data[0]["reasonText"] == flag_reason_text

    # Remove flag from post.
    remove_flag_q = """
    mutation RemoveFlag($post: Int!, $user: Int!){
      removeFlag(post: $post, user:$user) {
        postId
        userId
      }
    }
    """
    remove_flag_data = {
        "operationName": "RemoveFlag",
        "query": remove_flag_q.replace("\n", "").strip(),
        "variables": {"post": 5, "user": 1},
    }
    remove_flag_resp = client.post(
        "/api/graphql", headers=headers, data=json.dumps(remove_flag_data)
    )

    assert remove_flag_resp.status_code == 200

    remove_p_data = json.loads(remove_flag_resp.content)["data"]["removeFlag"]

    assert remove_p_data["postId"] == 5
    assert remove_p_data["userId"] == 1

    # Verify that the flag has been removed from the post.

    verify_r_resp = client.post(
        "/api/graphql", headers=headers, data=json.dumps(flag_q_data)
    )
    verify_r_data = json.loads(verify_r_resp.content)["data"]["flaggedPosts"]

    assert len(verify_r_data) == 0
