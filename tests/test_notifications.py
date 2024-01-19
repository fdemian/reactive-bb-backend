import json
import pytest
from .conftest import get_test_client


@pytest.mark.asyncio
async def test_add_mentions(setup_test_database):
    client = await get_test_client()
    from api.scripts.insert_test_data import user

    # Get credentials
    login_data = json.dumps(
        {"username": user["username"], "password": user["password"]}
    )
    login_resp = client.post("/api/login", data=login_data)
    access_token = login_resp.cookies["access_token"]

    # Verify that the user has no current notifications.
    notifications_query = """
    query Notifications($user: Int!) {
      notifications(user: $user) {
        id
        link
        type
        read
        originator {
          id
          avatar
          username
        }
        user {
          id
          avatar
          username
        }
      }
    }
    """
    notifications_data = {
        "operationName": "Notifications",
        "query": notifications_query.replace("\n", "").strip(),
        "variables": {"user": 1},
    }
    headers = {"content-type": "application/json", "access_token": access_token}
    notif_resp = client.post(
        "/api/graphql", headers=headers, data=json.dumps(notifications_data)
    )
    assert notif_resp.status_code == 200
    notif_content = json.loads(notif_resp.content)["data"]["notifications"]
    assert len(notif_content) == 0

    # Add mentions
    mentions_query = """
    mutation SetMentions($link: String!, $user: String!, $mentioned: [String!]) {
        setMentions(link: $link, user: $user, mentioned: $mentioned)
    }
    """
    mentions_data = {
        "operationName": "SetMentions",
        "query": mentions_query.replace("\n", "").strip(),
        "variables": {
            "link": "/topics/mention-test",
            "user": "user2",
            "mentioned": ["user"],
        },
    }
    mentions_resp = client.post(
        "/api/graphql", headers=headers, data=json.dumps(mentions_data)
    )

    assert mentions_resp.status_code == 200

    # Verify that we have new mentions
    notif_resp_mentions = client.post(
        "/api/graphql", headers=headers, data=json.dumps(notifications_data)
    )

    assert notif_resp_mentions.status_code == 200

    mentions_cont = json.loads(notif_resp_mentions.content)["data"]["notifications"]

    assert len(mentions_cont) == 1
    assert mentions_cont[0]["link"] == "/topics/mention-test"
    assert mentions_cont[0]["type"] == "mention"
    assert mentions_cont[0]["read"] == False
    assert mentions_cont[0]["originator"]["id"] == 2
    assert mentions_cont[0]["user"]["id"] == 1

    # Mark notification as read
    notification_id = int(mentions_cont[0]["id"])

    mark_read_query = """
    mutation MarkNotificationsRead($notifications: [Int!]) {
      markNotificationsRead(notifications: $notifications)
    }
    """
    mark_read_data = {
        "operationName": "MarkNotificationsRead",
        "query": mark_read_query.replace("\n", "").strip(),
        "variables": {"notifications": [notification_id]},
    }
    mark_read_resp = client.post(
        "/api/graphql", headers=headers, data=json.dumps(mark_read_data)
    )
    assert mark_read_resp.status_code == 200

    mark_read_cont = json.loads(mark_read_resp.content)["data"]["markNotificationsRead"]
    assert len(mark_read_cont) == 1  # There is only one notification marked as read.
    assert (
        mark_read_cont[0] == notification_id
    )  # The notification id is the same one we sent to the server.

    # Verify that there are no unread notifications.
    notify_resp = client.post(
        "/api/graphql", headers=headers, data=json.dumps(notifications_data)
    )
    assert notify_resp.status_code == 200
    notify_cont = json.loads(notify_resp.content)["data"]["notifications"]
    assert len(notify_cont) == 0

    # Get all notifications (read or unread)
    all_notif_query = """
    query AllNotifications($user: Int!, $limit: Int!, $offset: Int!) {
       allNotifications(user: $user, limit: $limit, offset: $offset) {
         id
         link
         type
         read
         originator {
           id
           avatar
           username
         }
         user {
           id
           avatar
           username
         }
       }
    }
    """
    all_notif_data = {
        "operationName": "AllNotifications",
        "query": all_notif_query.replace("\n", "").strip(),
        "variables": {"user": 1, "limit": 5, "offset": 0},
    }

    all_notif_resp = client.post(
        "/api/graphql", headers=headers, data=json.dumps(all_notif_data)
    )
    assert all_notif_resp.status_code == 200
    all_notif_cont = json.loads(all_notif_resp.content)["data"]["allNotifications"]
    assert len(all_notif_cont) == 1
    assert all_notif_cont[0]["id"] == notification_id
    assert all_notif_cont[0]["link"] == "/topics/mention-test"
    assert all_notif_cont[0]["type"] == "mention"
    assert all_notif_cont[0]["read"] == True
    assert all_notif_cont[0]["originator"]["id"] == 2
    assert all_notif_cont[0]["user"]["id"] == 1
