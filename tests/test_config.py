import json
import pytest
from .conftest import get_test_client


@pytest.mark.asyncio
async def test_default_config():
    client = await get_test_client()
    query = """query GetConfig {
      config {
        config
        oauth
        __typename
      }
    }"""
    data = {
        "operationName": "GetConfig",
        "query": query.replace("\n", "").strip(),
        "variables": {},
    }
    headers = {"content-type": "application/json"}
    response = client.post("/api/graphql", headers=headers, data=json.dumps(data))
    content = json.loads(response.content)
    data = content["data"]["config"]
    config = data["config"]
    oauth = data["oauth"]

    assert config["name"] == "Morpheus"
    assert config["description"] == "A web forum"
    assert int(config["items_per_page"]) == 10
    assert response.status_code == 200
    assert "redirectURI" in oauth
    assert "services" in oauth
