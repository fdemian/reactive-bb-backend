import pytest
import json
from .conftest import get_test_client


@pytest.mark.asyncio
async def test_chats(setup_test_database):
    client = await get_test_client()
    from api.scripts.insert_test_data import user

    # Get credentials.
    data = json.dumps({"username": user["username"], "password": user["password"]})
    login_resp = client.post("/api/login", data=data)
    access_token = login_resp.cookies["access_token"]
    headers = {"content-type": "application/json", "access_token": access_token}

    # Get chats by both users (both should have none).
    chats_query = """
    query GetChatsByUser($user: Int!) {
      chatsByUser(user: $user) {
        id
        avatar
        username
      }
    }
    """
    chats_data_1 = {
        "operationName": "GetChatsByUser",
        "query": chats_query.replace("\n", "").strip(),
        "variables": {"user": 1},
    }
    chats_data_2 = {
        "operationName": "GetChatsByUser",
        "query": chats_query.replace("\n", "").strip(),
        "variables": {"user": 1},
    }

    user_1_chats_resp = client.post(
        "/api/graphql", headers=headers, data=json.dumps(chats_data_1)
    )
    user_1_chats = json.loads(user_1_chats_resp.text)["data"]["chatsByUser"]
    user_2_chats_resp = client.post(
        "/api/graphql", headers=headers, data=json.dumps(chats_data_2)
    )
    user_2_chats = json.loads(user_2_chats_resp.text)["data"]["chatsByUser"]

    assert len(user_1_chats) == 0
    assert len(user_2_chats) == 0

    # Send new chat

    send_msg_query = """
    mutation SendMessage(
      $author: Int!
      $recipient: Int!
      $message: JSON!
      $newchat: Boolean!
    ) {
     sendMessage(
       author: $author
       recipient: $recipient
       message: $message
       newchat: $newchat
     )
    }
    """
    send_msg_data = {
        "operationName": "SendMessage",
        "query": send_msg_query.replace("\n", "").strip(),
        "variables": {"author": 1, "recipient": 2, "message": "{}", "newchat": True},
    }
    send_msg_resp = client.post(
        "/api/graphql", headers=headers, data=json.dumps(send_msg_data)
    )
    sent_msg = json.loads(send_msg_resp.text)["data"]["sendMessage"]

    assert sent_msg is True

    # Verify that new chat has been sent to both users.
    user_1_chats_resp_2 = client.post(
        "/api/graphql", headers=headers, data=json.dumps(chats_data_1)
    )
    user_1_chats_r = json.loads(user_1_chats_resp_2.text)["data"]["chatsByUser"]
    user_2_chats_resp_2 = client.post(
        "/api/graphql", headers=headers, data=json.dumps(chats_data_2)
    )
    user_2_chats_r = json.loads(user_2_chats_resp_2.text)["data"]["chatsByUser"]

    assert len(user_1_chats_r) == 1
    assert len(user_2_chats_r) == 1

    assert user_1_chats_r[0]["id"] == 2

    # Verify that the same is true for the actual chats.
    get_chats_query = """
    query GetChat($userA: Int!, $userB: Int!, $offset: Int!, $limit: Int!) {
      chat(userA: $userA, userB: $userB, offset: $offset, limit: $limit) {
        date
        content
        author {
          id
          avatar
          username
        }
        recipient {
          id
          avatar
          username
        }
      }
    }
    """
    get_chats_data = {
        "operationName": "GetChat",
        "query": get_chats_query.replace("\n", "").strip(),
        "variables": {"userA": 1, "userB": 2, "offset": 0, "limit": 5},
    }
    get_chats_resp = client.post(
        "/api/graphql", headers=headers, data=json.dumps(get_chats_data)
    )
    get_chats_cont = json.loads(get_chats_resp.text)["data"]["chat"]

    assert len(get_chats_cont) == 1
    assert get_chats_cont[0]["content"] == "{}"
    assert get_chats_cont[0]["author"]["id"] == 1
    assert get_chats_cont[0]["recipient"]["id"] == 2

    # Send another chat.
    send_msg_data_2 = {
        "operationName": "SendMessage",
        "query": send_msg_query.replace("\n", "").strip(),
        "variables": {"author": 2, "recipient": 1, "message": "{}", "newchat": False},
    }
    send_msg_resp_2 = client.post(
        "/api/graphql", headers=headers, data=json.dumps(send_msg_data_2)
    )
    sent_msg_2 = json.loads(send_msg_resp_2.text)["data"]["sendMessage"]
    assert sent_msg_2 is True

    # Verify that more than one message is present in the conversation.
    get_chats_resp = client.post(
        "/api/graphql", headers=headers, data=json.dumps(get_chats_data)
    )
    get_chats_cont = json.loads(get_chats_resp.text)["data"]["chat"]

    assert len(get_chats_cont) == 2
