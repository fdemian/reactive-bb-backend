import json
import pytest
from .file_utils import get_sample_file_contents, get_fr_data_headers
from .conftest import get_test_client


@pytest.mark.asyncio
async def test_upload_file(setup_test_database):
    client = await get_test_client()
    from api.scripts.insert_test_data import user

    # Get login credentials
    login_data = json.dumps(
        {"username": user["username"], "password": user["password"]}
    )
    login_resp = client.post("/api/login", data=login_data)
    access_token = login_resp.cookies["access_token"]

    upload_query = """
    mutation UploadImage($image: Upload!) {
      uploadImage(image: $image) {
       src
      }
    }
    """

    file_cont = get_sample_file_contents()
    req_headers = get_fr_data_headers(access_token)

    variables = {"image": None}

    upload_resp = client.post(
        "/api/graphql",
        data={
            "operations": json.dumps({"query": upload_query, "variables": variables}),
            "map": json.dumps({"0": ["variables.image"]}),
        },
        headers=req_headers,
        files={"0": (file_cont["name"], file_cont["content"], "image/png")},
    )
    assert upload_resp.status_code == 200
    upload_cont = json.loads(upload_resp.text)["data"]["uploadImage"]
    assert upload_cont["src"] == file_cont["name"]


@pytest.mark.asyncio
async def test_upload_file_no_permissions(setup_test_database):
    client = await get_test_client()

    upload_query = """
    mutation UploadImage($image: Upload!) {
      uploadImage(image: $image) {
       src
      }
    }
    """

    file_cont = get_sample_file_contents()
    req_headers = get_fr_data_headers("")
    del req_headers["access_token"]

    variables = {"image": None}

    upload_resp = client.post(
        "/api/graphql",
        data={
            "operations": json.dumps({"query": upload_query, "variables": variables}),
            "map": json.dumps({"0": ["variables.image"]}),
        },
        headers=req_headers,
        files={"0": (file_cont["name"], file_cont["content"], "image/png")},
    )

    upload_resp_cont = json.loads(upload_resp.text)
    upload_cont_data = upload_resp_cont["data"]["uploadImage"]
    upload_err = upload_resp_cont["errors"]

    assert upload_cont_data is None
    assert len(upload_err) > 0
    assert upload_err[0]["message"] == "Invalid auth credentials."
