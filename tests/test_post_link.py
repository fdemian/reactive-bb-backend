import json
import pytest
from .conftest import get_test_client


@pytest.mark.asyncio
async def test_search_posts(setup_test_database):
    client = await get_test_client()
    query = """  query GetPositionId($post: Int!, $itemscount: Int!) {
    postLink(post: $post, itemscount: $itemscount) {
      topicId
      page
      name
    }
  }"""

    data = {
        "operationName": "GetPositionId",
        "query": query.replace("\n", "").strip(),
        "variables": {"post": 1, "itemscount": 10},
    }

    headers = {"content-type": "application/json"}
    response = client.post("/api/graphql", headers=headers, data=json.dumps(data))
    respdata = json.loads(response.text)

    post_link = respdata["data"]["postLink"]

    assert response.status_code == 200
    assert post_link["topicId"] == 1
    assert post_link["page"] == 1
    assert post_link["name"] == "T-1000"
