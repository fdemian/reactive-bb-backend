import json
import pytest
from .file_utils import (
    get_sample_file_contents,
    get_sample_txt_contents,
    get_fr_data_headers,
)
from .conftest import get_test_client


@pytest.mark.asyncio
async def test_update_profile_pic(setup_test_database):
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
           }
       }"""

    data = {
        "operationName": "GetUser",
        "query": query.replace("\n", "").strip(),
        "variables": {"id": 1},
    }

    response = client.post("/api/graphql", headers=headers, data=json.dumps(data))
    user_resp_data = json.loads(response.text)["data"]["getUser"]

    assert user_resp_data["avatar"] is None

    # Upload profile pic
    update_query = """
       mutation UploadAvatar($image: Upload!, $id: Int!) {
          uploadUserImage(image: $image, id: $id) {
            id
            ok
          }
       }
       """
    file_cont = get_sample_file_contents()
    req_headers = get_fr_data_headers(access_token)

    variables = {"id": 1, "image": None}

    upload_resp = client.post(
        "/api/graphql",
        data={
            "operations": json.dumps({"query": update_query, "variables": variables}),
            "map": json.dumps({"1": ["variables.image"]}),
        },
        headers=req_headers,
        files={"1": (file_cont["name"], file_cont["content"], "image/png")},
    )

    assert upload_resp.status_code == 200
    upload_cont = json.loads(upload_resp.text)["data"]["uploadUserImage"]
    assert upload_cont["id"] == 1
    assert upload_cont["ok"] is True

    response = client.post("/api/graphql", headers=headers, data=json.dumps(data))
    user_resp_data = json.loads(response.text)["data"]["getUser"]

    assert user_resp_data["avatar"] == file_cont["name"]

    remove_query = """
       mutation removeAvatar($id: Int!) {
         removeUserImage(id: $id)
       }
       """

    remove_data = {
        "operationName": "removeAvatar",
        "query": remove_query.replace("\n", "").strip(),
        "variables": {"id": 1},
    }

    remove_resp = client.post(
        "/api/graphql", headers=headers, data=json.dumps(remove_data)
    )

    assert remove_resp.status_code == 200
    remove_cont = json.loads(remove_resp.text)
    assert remove_cont["data"]["removeUserImage"] is True

    response = client.post("/api/graphql", headers=headers, data=json.dumps(data))
    user_resp_data = json.loads(response.text)["data"]["getUser"]
    assert user_resp_data["avatar"] is None


@pytest.mark.asyncio
async def test_permissions_update_profile_pic(setup_test_database):
    client = await get_test_client()

    headers = {"content-type": "application/json"}

    query = """query GetUser($id: Int!) {
             getUser(id: $id) {
               id
               username
               avatar
             }
         }"""

    data = {
        "operationName": "GetUser",
        "query": query.replace("\n", "").strip(),
        "variables": {"id": 1},
    }

    response = client.post("/api/graphql", headers=headers, data=json.dumps(data))
    user_resp_data = json.loads(response.text)["data"]["getUser"]

    assert user_resp_data["avatar"] is None

    # Upload profile pic
    update_query = """
           mutation UploadAvatar($image: Upload!, $id: Int!) {
              uploadUserImage(image: $image, id: $id) {
                 id
                 ok
              }
           }
        """

    file_cont = get_sample_file_contents()
    req_headers = get_fr_data_headers("")

    variables = {"id": 1, "image": None}

    upload_resp = client.post(
        "/api/graphql",
        data={
            "operations": json.dumps({"query": update_query, "variables": variables}),
            "map": json.dumps({"1": ["variables.image"]}),
        },
        headers=req_headers,
        files={"1": (file_cont["name"], file_cont["content"], "image/png")},
    )

    upload_resp_err = json.loads(upload_resp.text)
    assert upload_resp_err["error"] is not None
    assert upload_resp_err["error"] == "Invalid auth credentials."

    remove_query = """
           mutation removeAvatar($id: Int!) {
             removeUserImage(id: $id)
           }
         """

    remove_data = {
        "operationName": "removeAvatar",
        "query": remove_query.replace("\n", "").strip(),
        "variables": {"id": 1},
    }
    remove_resp = client.post(
        "/api/graphql", headers=headers, data=json.dumps(remove_data)
    )

    assert remove_resp.status_code == 200
    remove_cont = json.loads(remove_resp.text)
    assert remove_cont["data"]["removeUserImage"] is None


@pytest.mark.asyncio
async def test_update_profile_pic_wrong_file_type(setup_test_database):
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
                 }
             }"""

    data = {
        "operationName": "GetUser",
        "query": query.replace("\n", "").strip(),
        "variables": {"id": 1},
    }

    response = client.post("/api/graphql", headers=headers, data=json.dumps(data))
    user_resp_data = json.loads(response.text)["data"]["getUser"]

    assert user_resp_data["avatar"] is None

    # Try to set the profile pic with the wrong file type.
    update_query = """
             mutation UploadAvatar($image: Upload!, $id: Int!) {
                uploadUserImage(image: $image, id: $id) {
                  id
                  ok
                }
             }
             """
    wrong_file_cont = get_sample_txt_contents()
    req_headers = get_fr_data_headers(access_token)

    variables = {"id": 1, "image": None}

    upload_resp = client.post(
        "/api/graphql",
        data={
            "operations": json.dumps({"query": update_query, "variables": variables}),
            "map": json.dumps({"1": ["variables.image"]}),
        },
        headers=req_headers,
        files={
            "1": (wrong_file_cont["name"], wrong_file_cont["content"], "text/plain")
        },
    )

    assert upload_resp.status_code == 200
    upload_cont = json.loads(upload_resp.text)["data"]["uploadUserImage"]
    assert upload_cont["id"] == 0
    assert upload_cont["ok"] is False

    # Check that user avatar is still not set.
    response = client.post("/api/graphql", headers=headers, data=json.dumps(data))
    user_resp_data = json.loads(response.text)["data"]["getUser"]

    assert user_resp_data["avatar"] is None
