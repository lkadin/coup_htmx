import json
from fastapi.testclient import TestClient
from app import app
import pytest


@pytest.fixture
def client():
    return TestClient(app)


def test_get_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_read_item(client):
    response = client.get("/web/1/?user_name=Lee")
    assert response.status_code == 200
    assert "Lee" in response.text


def test_websocket_connect(client):
    with client.websocket_connect("/ws/1") as websocket:
        data = {"message_txt": "Test message"}
        websocket.send_text(json.dumps(data))
        response = websocket.receive_text()
        assert "alert" in response
