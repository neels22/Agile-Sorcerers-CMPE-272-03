# Indraneel Sarode
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.fixture(scope="module")
def test_created_post():
    """Fixture to create a post and provide its details."""
    request_payload = {"content": "Test Post"}
    response = client.post("/post", json=request_payload)
    assert response.status_code == 200

    response_data = response.json()
    assert "id" in response_data
    assert "content" in response_data
    assert "created_at" in response_data
    assert response_data["content"] == request_payload["content"]
    return response_data

def test_get_post_ids(test_created_post):
    """Test that the created post ID exists in the list of post IDs."""
    test_created_post_id = test_created_post["id"]
    
    response = client.get("/post_ids")
    assert response.status_code == 200
    response_data = response.json()
    
    assert test_created_post_id in response_data["ids"]

def test_get_post(test_created_post):
    """Test retrieving the post using the created post ID."""
    post_id = test_created_post["id"]
    response = client.get(f"/post/{post_id}")
    assert response.status_code == 200

    response_data = response.json()
    assert response_data["id"] == post_id
    assert "content" in response_data
    assert "created_at" in response_data
    assert response_data["content"] == test_created_post["content"]

def test_delete_post(test_created_post):
    """Test deleting the post using the created post ID."""
    post_id = test_created_post["id"]
    response = client.delete(f"/post/{post_id}")
    assert response.status_code == 200

    response_data = response.json()
    assert response_data["message"] == "Post deleted"

    response = client.get("/post_ids")
    response_data = response.json()
    assert post_id not in response_data["ids"]
