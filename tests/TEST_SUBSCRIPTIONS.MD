Ariadne's test suite contains examples of how subscriptions can be tested:

from starlette.testclient import TestClient

from ariadne.asgi import (
    GQL_CONNECTION_ACK,
    GQL_CONNECTION_ERROR,
    GQL_CONNECTION_INIT,
    GQL_CONNECTION_TERMINATE,
    GQL_START,
    GQL_DATA,
    GQL_STOP,
    GQL_COMPLETE,
    GraphQL,
    WebSocketConnectionError,
)


def test_field_can_be_subscribed_using_websocket_connection(client):
    with client.websocket_connect("/", "graphql-ws") as ws:
        ws.send_json({"type": GQL_CONNECTION_INIT})
        ws.send_json(
            {
                "type": GQL_START,
                "id": "test1",
                "payload": {"query": "subscription { ping }"},
            }
        )
        response = ws.receive_json()
        assert response["type"] == GQL_CONNECTION_ACK
        response = ws.receive_json()
        assert response["type"] == GQL_DATA
        assert response["id"] == "test1"
        assert response["payload"]["data"] == {"ping": "pong"}
        ws.send_json({"type": GQL_STOP, "id": "test1"})
        response = ws.receive_json()
        assert response["type"] == GQL_COMPLETE
        assert response["id"] == "test1"
        ws.send_json({"type": GQL_CONNECTION_TERMINATE})

From my understanding fastapi.testclient.TestClient is actually an alias for starlette.testclient.TestClient, so test should be same for both of those libs.