import json
import pytest
from .conftest import get_test_client


@pytest.mark.asyncio
async def test_get_mention_candidates(setup_test_database):
    client = await get_test_client()
    query = """query GetMentionCandidates($search: String!) {
      mentionCandidates(search: $search) {
       id
       username
       avatar
       banned
       banReason
       lockoutTime
      }
    }"""

    data = {
        "operationName": "GetMentionCandidates",
        "query": query.replace("\n", "").strip(),
        "variables": {
            "search": "user",
        },
    }
    headers = {"content-type": "application/json"}

    response = client.post("/api/graphql", headers=headers, data=json.dumps(data))
    respdata = json.loads(response.content)

    candidates = respdata["data"]["mentionCandidates"]
    candidate = candidates[0]
    assert response.status_code == 200
    assert len(candidates) == 2
    assert candidate["id"] == 1
    assert candidate["username"] == "user"
    assert candidate["avatar"] is None
    assert candidate["banned"] is False
    assert candidate["banReason"] is None
    assert candidate["lockoutTime"] is None
