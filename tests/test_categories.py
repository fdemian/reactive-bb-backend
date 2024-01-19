import json
import pytest
from .conftest import get_test_client


@pytest.mark.asyncio
async def test_get_categories(setup_test_database):
    client = await get_test_client()


    query = """query GetCategories {
      categories {
        id
        name
        description
        __typename
      }
    }
    """
    data = {
        "operationName": "GetCategories",
        "query": query.replace("\n", "").strip(),
        "variables": {},
    }
    headers = {"content-type": "application/json"}
    response = client.post("/api/graphql", headers=headers, data=json.dumps(data))
    content = json.loads(response.content)
    categories = content["data"]["categories"]
    assert response.status_code == 200
    assert len(categories) == 1


@pytest.mark.asyncio
async def test_get_category(setup_test_database):
    client = await get_test_client()


    query = """query GetCategory($id: Int!) {
        category(id: $id) {
          id
          name
          description
          topics {
            id
            name
            views
            replies
            created
            pinned
            closed
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
        }
    }
    """

    data = {
        "operationName": "GetCategory",
        "query": query.replace("\n", "").strip(),
        "variables": {"id": 1},
    }
    headers = {"content-type": "application/json"}
    response = client.post("/api/graphql", headers=headers, data=json.dumps(data))
    content = json.loads(response.content)
    category = content["data"]["category"]

    assert response.status_code == 200
    assert category["id"] == 1
    assert category["name"] == "A category"
    assert category["description"] == "A description"
    assert len(category["topics"]) == 1


@pytest.mark.asyncio
async def test_create_category(setup_test_database):
    client = await get_test_client()

    from api.scripts.insertdata.insert_user import user

    # Get login credentials
    login_data = json.dumps(
        {"username": user["username"], "password": user["password"]}
    )
    login_resp = client.post("/api/login", data=login_data)
    access_token = login_resp.cookies["access_token"]

    headers = {"content-type": "application/json", "access_token": access_token}

    # Create new category

    category_name = "A new category"
    category_desc = "A new category description"

    create_cat_query = """
    mutation CreateCategory($name: String!, $description: String!) {
      createCategory(name: $name, description: $description) {
        id
        name
        description
      }
    }
    """
    create_cat_data = {
        "operationName": "CreateCategory",
        "query": create_cat_query.replace("\n", "").strip(),
        "variables": {"name": category_name, "description": category_desc},
    }

    create_resp = client.post(
        "/api/graphql", headers=headers, data=json.dumps(create_cat_data)
    )
    assert create_resp.status_code == 200

    create_cont = json.loads(create_resp.content)
    created_cat = create_cont["data"]["createCategory"]

    assert created_cat["name"] == category_name
    assert created_cat["description"] == category_desc

    # Verify that category has been created.
    category_id = created_cat["id"]
    get_cat_query = """query GetCategory($id: Int!) {
        category(id: $id) {
          id
          name
          description
        }
    }
    """

    get_cat_data = {
        "operationName": "GetCategory",
        "query": get_cat_query.replace("\n", "").strip(),
        "variables": {"id": category_id},
    }
    get_cat_resp = client.post(
        "/api/graphql", headers=headers, data=json.dumps(get_cat_data)
    )

    assert get_cat_resp.status_code == 200
    cat_content = json.loads(get_cat_resp.content)["data"]["category"]

    assert cat_content["id"] == category_id
    assert cat_content["name"] == category_name
    assert cat_content["description"] == category_desc
