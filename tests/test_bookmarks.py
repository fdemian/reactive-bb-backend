import json
import pytest
from .conftest import get_test_client


@pytest.mark.asyncio
async def test_get_set_delete_bookmarks(setup_test_database):
    client = await get_test_client()
    from api.scripts.insert_test_data import user

    # Get login credentials
    login_data = json.dumps(
        {"username": user["username"], "password": user["password"]}
    )
    login_resp = client.post("/api/login", data=login_data)
    access_token = login_resp.cookies["access_token"]

    query = """query GetBookmarksByUser($user: Int!) {
      bookmarksByUser(user: $user) {
       id
       post {
         id
         content
         user {
           id
           username
           avatar
         }
       }
       }
    }"""

    data = {
        "operationName": "GetBookmarksByUser",
        "query": query.replace("\n", "").strip(),
        "variables": {
            "user": 1,
        },
    }
    headers = {"content-type": "application/json"}
    response = client.post("/api/graphql", headers=headers, data=json.dumps(data))

    assert response.status_code == 200
    resp_data = json.loads(response.content)["data"]["bookmarksByUser"]
    assert len(resp_data) == 0

    add_bookmark_query = """
    mutation BookmarkPost($user: Int!, $post: Int!) {
      bookmarkPost(user: $user, post: $post) {
        id
        ok
        postId
        userId
      }
    }
    """
    add_bookmark_data = {
        "operationName": "BookmarkPost",
        "query": add_bookmark_query.replace("\n", "").strip(),
        "variables": {"user": 1, "post": 1},
    }

    headers_mut = {"content-type": "application/json", "access_token": access_token}
    response_mut = client.post(
        "/api/graphql", headers=headers_mut, data=json.dumps(add_bookmark_data)
    )

    assert response_mut.status_code == 200
    mut_cont = json.loads(response_mut.content)
    mut_data = mut_cont["data"]["bookmarkPost"]

    assert mut_data["ok"] is True
    assert mut_data["id"] == 1
    assert mut_data["userId"] == 1

    # Check that post has been bookmarked.
    add_resp = client.post("/api/graphql", headers=headers, data=json.dumps(data))
    assert add_resp.status_code == 200
    add_cont = json.loads(add_resp.content)["data"]["bookmarksByUser"]

    assert len(add_cont) == 1
    assert add_cont[0]["post"]["id"] == 1
    assert add_cont[0]["post"]["user"]["id"] == 1

    # Remove bookmark from the post.
    remove_query = """
    mutation RemoveBookmark($user: Int!, $post: Int!) {
      removeBookmark(user: $user, post: $post) {
        id
        ok
        postId
        userId
      }
    }
    """
    remove_data = {
        "operationName": "RemoveBookmark",
        "query": remove_query.replace("\n", "").strip(),
        "variables": {"user": 1, "post": 1},
    }
    remove_mut_resp = client.post(
        "/api/graphql", headers=headers_mut, data=json.dumps(remove_data)
    )
    assert remove_mut_resp.status_code == 200
    remove_mut_cont = json.loads(remove_mut_resp.content)["data"]["removeBookmark"]

    assert remove_mut_cont["ok"] is True
    assert remove_mut_cont["id"] == 1
    assert remove_mut_cont["postId"] == 1
    assert remove_mut_cont["userId"] == 1

    # Verify that the bookmark has been successfully removed.
    final_verif_resp = client.post(
        "/api/graphql", headers=headers, data=json.dumps(data)
    )
    assert final_verif_resp.status_code == 200
    final_verif_data = json.loads(response.content)["data"]["bookmarksByUser"]
    assert len(final_verif_data) == 0


@pytest.mark.asyncio
async def test_bookmarks_by_user_posts(setup_test_database):
    client = await get_test_client()
    from api.scripts.insert_test_data import user

    # Get login credentials
    login_data = json.dumps(
        {"username": user["username"], "password": user["password"]}
    )
    login_resp = client.post("/api/login", data=login_data)
    access_token = login_resp.cookies["access_token"]

    query = """ query GetBookmarksByPosts($user: Int!, $posts: [Int!]) {
    bookmarksByPostList(user: $user, posts: $posts) {
      id
      userId
      postId
    }
     }"""

    data = {
        "operationName": "GetBookmarksByPosts",
        "query": query.replace("\n", "").strip(),
        "variables": {"user": 2, "posts": [1, 2]},
    }
    headers = {"content-type": "application/json"}
    response = client.post("/api/graphql", headers=headers, data=json.dumps(data))

    assert response.status_code == 200
    resp_data = json.loads(response.content)["data"]["bookmarksByPostList"]
    assert len(resp_data) == 0

    add_bookmark_query = """
    mutation BookmarkPost($user: Int!, $post: Int!) {
      bookmarkPost(user: $user, post: $post) {
        id
        ok
        postId
        userId
      }
    }
    """
    add_bookmark_data = {
        "operationName": "BookmarkPost",
        "query": add_bookmark_query.replace("\n", "").strip(),
        "variables": {"user": 2, "post": 1},
    }
    headers_mut = {"content-type": "application/json", "access_token": access_token}
    response_mut = client.post(
        "/api/graphql", headers=headers_mut, data=json.dumps(add_bookmark_data)
    )

    assert response_mut.status_code == 200
    mut_cont = json.loads(response_mut.content)
    mut_data = mut_cont["data"]["bookmarkPost"]

    assert mut_data["ok"] is True
    assert mut_data["id"] == 1
    assert mut_data["userId"] == 2

    # Check that post has been bookmarked.
    check_bk_resp = client.post("/api/graphql", headers=headers, data=json.dumps(data))
    assert check_bk_resp.status_code == 200
    check_bk_cont = json.loads(check_bk_resp.content)["data"]["bookmarksByPostList"]
    assert len(check_bk_cont) == 1
    assert check_bk_cont[0]["id"] == 1
    assert check_bk_cont[0]["userId"] == 2
    assert check_bk_cont[0]["postId"] == 1
