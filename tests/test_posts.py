import json
import pytest
from .conftest import get_test_client


@pytest.mark.asyncio
async def test_get_posts(setup_test_database):
    client = await get_test_client()

    query = """query GetPosts($topicId: Int!, $limit: Int!, $offset: Int!) {
    posts(topicId: $topicId, limit: $limit, offset: $offset) {
       id
       content
       created
       likes {
         id
         userId
         postId
       }
       user {
         id
         avatar
         username
         status
       }
      }
    }"""

    data = {
        "operationName": "GetPosts",
        "query": query.replace("\n", "").strip(),
        "variables": {"topicId": 1, "limit": 5, "offset": 0},
    }
    headers = {"content-type": "application/json"}
    response = client.post("/api/graphql", headers=headers, data=json.dumps(data))
    respdata = json.loads(response.content)
    posts = respdata["data"]["posts"]

    assert response.status_code == 200
    assert len(posts) == 5
    assert posts[0]["id"] == 1
    assert posts[0]["user"]["id"] == 1
    assert posts[0]["content"] is not None
    assert posts[0]["created"] is not None
    assert len(posts[0]["likes"]) == 0


@pytest.mark.asyncio
async def test_get_posts_by_user(setup_test_database):
    client = await get_test_client()
    query = """query GetPostsByUser($id: Int!) {
      postsByUser(id: $id) {
        id
        content
        topicId
      }
    }"""

    data = {
        "operationName": "GetPostsByUser",
        "query": query.replace("\n", "").strip(),
        "variables": {"id": 1},
    }
    headers = {"content-type": "application/json"}
    response = client.post("/api/graphql", headers=headers, data=json.dumps(data))
    respdata = json.loads(response.content)
    posts = respdata["data"]["postsByUser"]

    assert response.status_code == 200
    assert len(posts) == 1000

    for post in posts:
        assert post["content"] is not None
        assert post["topicId"] is not None


@pytest.mark.asyncio
async def test_create_post(setup_test_database):
    client = await get_test_client()
    from api.scripts.insert_test_data import user

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
        "variables": {"id": 1},
    }
    headers = {"content-type": "application/json"}
    response = client.post("/api/graphql", headers=headers, data=json.dumps(data))
    respdata = json.loads(response.content)
    topic = respdata["data"]["topic"]

    assert topic["replies"] == 1000

    #
    add_p_query = """mutation AddPost($user: Int!, $topic: Int!, $content: JSON!) {
         createPost(user: $user, topic: $topic, content: $content) {
           content
           user {
             id
             avatar
             username
           }
         }
     }"""

    add_p_data = {
        "operationName": "AddPost",
        "query": add_p_query.replace("\n", "").strip(),
        "variables": {"user": 1, "topic": 1, "content": "{}"},
    }
    add_post_headers = {
        "content-type": "application/json",
        "access_token": access_token,
    }
    add_p_response = client.post(
        "/api/graphql", headers=add_post_headers, data=json.dumps(add_p_data)
    )
    assert add_p_response.status_code == 200

    # Get topic and check that the new reply/post has been added.

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

    assert topic["replies"] == 1001


@pytest.mark.asyncio
async def test_edit_post(setup_test_database):
    client = await get_test_client()
    from api.scripts.insert_test_data import mod_user

    #
    query = """query GetPosts($topicId: Int!, $limit: Int!, $offset: Int!) {
    posts(topicId: $topicId, limit: $limit, offset: $offset) {
       id
       content
       created
       likes {
         id
         userId
         postId
       }
       user {
         id
         avatar
         username
         status
       }
      }
    }"""

    data = {
        "operationName": "GetPosts",
        "query": query.replace("\n", "").strip(),
        "variables": {"topicId": 1, "limit": 5, "offset": 0},
    }
    headers = {"content-type": "application/json"}
    response = client.post("/api/graphql", headers=headers, data=json.dumps(data))
    resp_data = json.loads(response.content)
    posts = resp_data["data"]["posts"]

    post_to_edit = posts[0]

    next_post_content = (
        '{"root":{"children":[{"children":[{"detail":0,"format":0,"mode":"normal","style":"","text":"Post#'
        + str(40)
        + '","type":"text","version":1}],"direction":"ltr","format":"","indent":0,"type":"paragraph","version":1}],"direction":"ltr","format":"","indent":0,"type":"root","version":1}}'
    )
    prev_post_content = post_to_edit["content"]

    assert response.status_code == 200
    assert post_to_edit["content"] is not next_post_content

    # Get access token.
    login_data = json.dumps(
        {"username": mod_user["username"], "password": mod_user["password"]}
    )
    login_resp = client.post("/api/login", data=login_data)
    access_token = login_resp.cookies["access_token"]

    edit_mutation = """
    mutation EditPost($post: Int!, $user: Int!, $content: JSON!) {
      editPost(post: $post, user: $user, content: $content) {
        id
        ok
        content
        __typename
      }
    }
    """
    edit_data = {
        "operationName": "EditPost",
        "query": edit_mutation.replace("\n", "").strip(),
        "variables": {
            "post": post_to_edit["id"],
            "user": 1,
            "content": next_post_content,
        },
    }
    edit_headers = {"content-type": "application/json", "access_token": access_token}
    edit_resp = client.post(
        "/api/graphql", headers=edit_headers, data=json.dumps(edit_data)
    )
    assert edit_resp.status_code == 200

    edit_cont = json.loads(edit_resp.content)["data"]["editPost"]

    assert edit_cont["id"] == post_to_edit["id"]
    assert edit_cont["ok"] is True
    assert edit_cont["content"] == next_post_content

    # Refetch topic posts
    response = client.post("/api/graphql", headers=headers, data=json.dumps(data))
    resp_data = json.loads(response.content)
    posts = resp_data["data"]["posts"]

    edited_post = next((p for p in posts if p["id"] == post_to_edit["id"]), None)

    assert edited_post is not None
    assert edited_post["content"] is not prev_post_content
    assert edited_post["content"] == next_post_content


@pytest.mark.asyncio
async def test_view_edited_posts(setup_test_database):
    client = await get_test_client()
    from api.scripts.insert_test_data import admin_user

    #
    query = """query GetPosts($topicId: Int!, $limit: Int!, $offset: Int!) {
    posts(topicId: $topicId, limit: $limit, offset: $offset) {
       id
       content
       created
       likes {
         id
         userId
         postId
       }
       user {
         id
         avatar
         username
         status
       }
      }
    }"""

    data = {
        "operationName": "GetPosts",
        "query": query.replace("\n", "").strip(),
        "variables": {"topicId": 1, "limit": 5, "offset": 0},
    }
    headers = {"content-type": "application/json"}
    response = client.post("/api/graphql", headers=headers, data=json.dumps(data))
    resp_data = json.loads(response.content)
    posts = resp_data["data"]["posts"]

    post_to_edit = posts[0]

    next_post_content = (
        '{"root":{"children":[{"children":[{"detail":0,"format":0,"mode":"normal","style":"","text":"Post#'
        + str(40)
        + '","type":"text","version":1}],"direction":"ltr","format":"","indent":0,"type":"paragraph","version":1}],"direction":"ltr","format":"","indent":0,"type":"root","version":1}}'
    )
    prev_post_content = post_to_edit["content"]

    assert response.status_code == 200
    assert post_to_edit["content"] is not next_post_content

    # Get access token.
    login_data = json.dumps(
        {"username": admin_user["username"], "password": admin_user["password"]}
    )
    login_resp = client.post("/api/login", data=login_data)
    access_token = login_resp.cookies["access_token"]

    edit_mutation = """
    mutation EditPost($post: Int!, $user: Int!, $content: JSON!) {
      editPost(post: $post, user: $user, content: $content) {
        id
        ok
        content
        __typename
      }
    }
    """
    edit_data = {
        "operationName": "EditPost",
        "query": edit_mutation.replace("\n", "").strip(),
        "variables": {
            "post": post_to_edit["id"],
            "user": 1,
            "content": next_post_content,
        },
    }
    edit_headers = {"content-type": "application/json", "access_token": access_token}
    edit_resp = client.post(
        "/api/graphql", headers=edit_headers, data=json.dumps(edit_data)
    )
    assert edit_resp.status_code == 200

    edit_cont = json.loads(edit_resp.content)["data"]["editPost"]

    assert edit_cont["id"] == post_to_edit["id"]
    assert edit_cont["ok"] is True
    assert edit_cont["content"] == next_post_content

    # Fetch edited posts list

    get_edits_mutation = """
    query PostEdits($limit: Int!, $offset: Int!) {
        postEdits(limit: $limit, offset: $offset) {
        postEdits {
          user {
           id
           avatar
           username
          }
          date
          previous
          current
        }
        editsCount
      }
    }
    """

    get_post_edit_data = {
        "operationName": "PostEdits",
        "query": get_edits_mutation.replace("\n", "").strip(),
        "variables": {"limit": 5, "offset": 0},
    }

    response = client.post(
        "/api/graphql", headers=edit_headers, data=json.dumps(get_post_edit_data)
    )
    resp_data = json.loads(response.content)
    post_edits_cont = resp_data["data"]["postEdits"]
    post_edits = post_edits_cont["postEdits"]
    post_edits_count = post_edits_cont["editsCount"]

    assert post_edits_count == 1
    assert post_edits[0]["user"]["id"] == 1
    assert post_edits[0]["previous"] == prev_post_content
    assert post_edits[0]["current"] == next_post_content


@pytest.mark.asyncio
async def test_view_edited_posts_fail_mod(setup_test_database):
    client = await get_test_client()
    from api.scripts.insert_test_data import user, mod_user

    #
    query = """query GetPosts($topicId: Int!, $limit: Int!, $offset: Int!) {
    posts(topicId: $topicId, limit: $limit, offset: $offset) {
       id
       content
       created
       likes {
         id
         userId
         postId
       }
       user {
         id
         avatar
         username
         status
       }
      }
    }"""

    data = {
        "operationName": "GetPosts",
        "query": query.replace("\n", "").strip(),
        "variables": {"topicId": 1, "limit": 5, "offset": 0},
    }
    headers = {"content-type": "application/json"}
    response = client.post("/api/graphql", headers=headers, data=json.dumps(data))
    resp_data = json.loads(response.content)
    posts = resp_data["data"]["posts"]

    post_to_edit = posts[0]

    next_post_content = (
        '{"root":{"children":[{"children":[{"detail":0,"format":0,"mode":"normal","style":"","text":"Post#'
        + str(40)
        + '","type":"text","version":1}],"direction":"ltr","format":"","indent":0,"type":"paragraph","version":1}],"direction":"ltr","format":"","indent":0,"type":"root","version":1}}'
    )
    prev_post_content = post_to_edit["content"]

    assert response.status_code == 200
    assert post_to_edit["content"] is not next_post_content

    # Get mod access token.
    login_data = json.dumps(
        {"username": mod_user["username"], "password": mod_user["password"]}
    )
    login_resp = client.post("/api/login", data=login_data)
    access_token = login_resp.cookies["access_token"]

    edit_mutation = """
    mutation EditPost($post: Int!, $user: Int!, $content: JSON!) {
      editPost(post: $post, user: $user, content: $content) {
        id
        ok
        content
        __typename
      }
    }
    """
    edit_data = {
        "operationName": "EditPost",
        "query": edit_mutation.replace("\n", "").strip(),
        "variables": {
            "post": post_to_edit["id"],
            "user": 1,
            "content": next_post_content,
        },
    }
    edit_headers = {"content-type": "application/json", "access_token": access_token}
    edit_resp = client.post(
        "/api/graphql", headers=edit_headers, data=json.dumps(edit_data)
    )
    assert edit_resp.status_code == 200

    edit_cont = json.loads(edit_resp.content)["data"]["editPost"]

    assert edit_cont["id"] == post_to_edit["id"]
    assert edit_cont["ok"] is True
    assert edit_cont["content"] == next_post_content

    # Fetch edited posts list

    get_edits_mutation = """
    query PostEdits($limit: Int!, $offset: Int!) {
        postEdits(limit: $limit, offset: $offset) {
        postEdits {
          user {
           id
           avatar
           username
          }
          date
          previous
          current
        }
        editsCount
      }
    }
    """

    get_post_edit_data = {
        "operationName": "PostEdits",
        "query": get_edits_mutation.replace("\n", "").strip(),
        "variables": {"limit": 5, "offset": 0},
    }

    response = client.post(
        "/api/graphql", headers=edit_headers, data=json.dumps(get_post_edit_data)
    )
    resp_data = json.loads(response.content)

    post_edits_content = resp_data["data"]["postEdits"]
    post_edit_errors = resp_data["errors"]
    assert post_edits_content is None
    assert post_edit_errors[0]["message"] == "Invalid permissions"

    # Test failure for user

    login_data_user = json.dumps(
        {"username": user["username"], "password": user["password"]}
    )
    login_resp_user = client.post("/api/login", data=login_data_user)
    access_token_user = login_resp_user.cookies["access_token"]
    edit_headers_user = {
        "content-type": "application/json",
        "access_token": access_token_user,
    }
    response = client.post(
        "/api/graphql", headers=edit_headers_user, data=json.dumps(get_post_edit_data)
    )
    resp_data = json.loads(response.content)

    post_edits_content = resp_data["data"]["postEdits"]
    post_edit_errors = resp_data["errors"]
    assert post_edits_content is None
    assert post_edit_errors[0]["message"] == "Invalid permissions"


@pytest.mark.asyncio
async def test_delete_post(setup_test_database):
    client = await get_test_client()
    from api.scripts.insert_test_data import mod_user

    id_to_delete = 1

    # Get credentials
    login_data = json.dumps(
        {"username": mod_user["username"], "password": mod_user["password"]}
    )
    login_resp = client.post("/api/login", data=login_data)
    access_token = login_resp.cookies["access_token"]

    # Check that post id to delete

    link_query = """  query GetPositionId($post: Int!, $itemscount: Int!) {
      postLink(post: $post, itemscount: $itemscount) {
        topicId
        page
        name
      }
    }"""
    link_data = {
        "operationName": "GetPositionId",
        "query": link_query.replace("\n", "").strip(),
        "variables": {"post": 1, "itemscount": 10},
    }
    headers = {"content-type": "application/json"}
    response = client.post("/api/graphql", headers=headers, data=json.dumps(link_data))
    assert response.status_code == 200
    link_content = json.loads(response.content)

    assert link_content["data"] is not None
    assert link_content["data"]["postLink"] is not None

    # Delete post
    delete_mutation = """mutation DeletePost($post: Int!, $user: Int!) {
      deletePost(post: $post, user: $user) {
        ok
        id
      }
    }
    """

    delete_data = {
        "operationName": "DeletePost",
        "query": delete_mutation.replace("\n", "").strip(),
        "variables": {"post": id_to_delete, "user": 1},
    }
    delete_headers = {"content-type": "application/json", "access_token": access_token}
    delete_resp = client.post(
        "/api/graphql", headers=delete_headers, data=json.dumps(delete_data)
    )
    delete_resp_data = json.loads(delete_resp.content)["data"]["deletePost"]

    assert delete_resp.status_code == 200
    assert delete_resp_data["ok"] is True
    assert delete_resp_data["id"] == id_to_delete

    # Check that post has been deleted
    check_resp = client.post(
        "/api/graphql", headers=headers, data=json.dumps(link_data)
    )
    check_content = json.loads(check_resp.content)

    assert check_content["data"] is None
    assert len(check_content["errors"]) > 0


@pytest.mark.asyncio
async def test_cant_delete_post(setup_test_database):
    client = await get_test_client()
    from api.scripts.insert_test_data import user

    id_to_delete = 1

    # Get credentials
    login_data = json.dumps(
        {"username": user["username"], "password": user["password"]}
    )
    login_resp = client.post("/api/login", data=login_data)
    access_token = login_resp.cookies["access_token"]

    # Try to delete post
    delete_mutation = """mutation DeletePost($post: Int!, $user: Int!) {
      deletePost(post: $post, user: $user) {
        ok
        id
      }
    }
    """

    delete_data = {
        "operationName": "DeletePost",
        "query": delete_mutation.replace("\n", "").strip(),
        "variables": {"post": id_to_delete, "user": 1},
    }
    delete_headers = {"content-type": "application/json", "access_token": access_token}
    delete_resp = client.post(
        "/api/graphql", headers=delete_headers, data=json.dumps(delete_data)
    )
    delete_resp_data = json.loads(delete_resp.content)["data"]["deletePost"]

    assert delete_resp.status_code == 200
    assert delete_resp_data is None


@pytest.mark.asyncio
async def test_edit_post_fail(setup_test_database):
    client = await get_test_client()
    from api.scripts.insert_test_data import user

    #
    query = """query GetPosts($topicId: Int!, $limit: Int!, $offset: Int!) {
    posts(topicId: $topicId, limit: $limit, offset: $offset) {
       id
       content
       created
       likes {
         id
         userId
         postId
       }
       user {
         id
         avatar
         username
         status
       }
      }
    }"""

    data = {
        "operationName": "GetPosts",
        "query": query.replace("\n", "").strip(),
        "variables": {"topicId": 1, "limit": 5, "offset": 0},
    }
    headers = {"content-type": "application/json"}
    response = client.post("/api/graphql", headers=headers, data=json.dumps(data))
    resp_data = json.loads(response.content)
    posts = resp_data["data"]["posts"]

    post_to_edit = posts[0]

    next_post_content = (
        '{"root":{"children":[{"children":[{"detail":0,"format":0,"mode":"normal","style":"","text":"Post#'
        + str(40)
        + '","type":"text","version":1}],"direction":"ltr","format":"","indent":0,"type":"paragraph","version":1}],"direction":"ltr","format":"","indent":0,"type":"root","version":1}}'
    )
    prev_post_content = post_to_edit["content"]

    assert response.status_code == 200
    assert post_to_edit["content"] is not next_post_content

    # Get access token.
    login_data = json.dumps(
        {"username": user["username"], "password": user["password"]}
    )
    login_resp = client.post("/api/login", data=login_data)
    access_token = login_resp.cookies["access_token"]

    edit_mutation = """
    mutation EditPost($post: Int!, $user: Int!, $content: JSON!) {
      editPost(post: $post, user: $user, content: $content) {
        id
        ok
        content
        __typename
      }
    }
    """
    edit_data = {
        "operationName": "EditPost",
        "query": edit_mutation.replace("\n", "").strip(),
        "variables": {
            "post": post_to_edit["id"],
            "user": 1,
            "content": next_post_content,
        },
    }
    edit_headers = {"content-type": "application/json", "access_token": access_token}
    edit_resp = client.post(
        "/api/graphql", headers=edit_headers, data=json.dumps(edit_data)
    )
    assert edit_resp.status_code == 200

    edit_cont = json.loads(edit_resp.content)

    assert len(edit_cont["errors"]) == 1
    assert edit_cont["data"]["editPost"] is None
    assert edit_cont["errors"][0]["message"] == "Invalid permissions"

    # Refetch topic posts
    response = client.post("/api/graphql", headers=headers, data=json.dumps(data))
    resp_data = json.loads(response.content)
    posts = resp_data["data"]["posts"]

    # Check that the post has not been edited, and that its contents remain unchanged.
    edited_post = next((p for p in posts if p["id"] == post_to_edit["id"]), None)

    assert edited_post is not None
    assert edited_post["content"] == prev_post_content
    assert edited_post["content"] is not next_post_content
