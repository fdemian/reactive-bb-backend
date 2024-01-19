import json
import pytest
from .conftest import get_test_client


@pytest.mark.asyncio
async def test_password_reset(setup_test_database):
    client = await get_test_client()
    from api.scripts.insert_test_data import user
    from .helpers import get_user_reset_token

    new_pass = user["password"] + "_X"

    # Test that current password works.
    data = json.dumps({"username": user["username"], "password": user["password"]})
    login_resp = client.post("/api/login", data=data)
    login_cont = json.loads(login_resp.text)
    assert login_resp.status_code == 200
    assert login_cont["ok"] is True
    assert login_cont["id"] == 1

    headers = {"content-type": "application/json"}
    req_res_query = """mutation ResetPasswordRequest($email: String!) {
       resetPasswordRequest(email: $email)
    }"""

    req_res_data = {
        "operationName": "ResetPasswordRequest",
        "query": req_res_query.replace("\n", "").strip(),
        "variables": {"email": user["email"]},
    }
    client.post("/api/graphql", headers=headers, data=json.dumps(req_res_data))
    reset_token = get_user_reset_token(user["email"])

    reset_query = """mutation ResetPassword($token: String!, $password: String!) {
        resetPassword(token: $token, password: $password)
    }"""

    reset_data = {
        "operationName": "ResetPassword",
        "query": reset_query.replace("\n", "").strip(),
        "variables": {"token": reset_token, "password": new_pass},
    }
    reset_resp = client.post(
        "/api/graphql", headers=headers, data=json.dumps(reset_data)
    )
    resp_cont = json.loads(reset_resp.text)["data"]["resetPassword"]
    assert resp_cont is True

    # Test that the old password does not work afer the password reset.
    login_resp = client.post("/api/login", data=data)
    login_cont = json.loads(login_resp.text)
    assert login_resp.status_code == 200
    assert login_cont["ok"] is False
    assert login_cont["id"] is None

    # Test that the new password does work
    data_2 = json.dumps({"username": user["username"], "password": new_pass})
    login_resp_2 = client.post("/api/login", data=data_2)
    login_cont_2 = json.loads(login_resp_2.text)
    assert login_resp.status_code == 200
    assert login_cont_2["ok"] is True
    assert login_cont_2["id"] == 1
