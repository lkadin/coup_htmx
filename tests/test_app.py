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
    assert "Assassinate" in response.text
    assert "Coup" in response.text
    assert "Steal" in response.text
    assert "Take_3_coins" in response.text
    assert "Foreign_aid" in response.text
    assert "Income" in response.text
    assert "Exchange" in response.text
    assert "Block" in response.text
    assert "Challenge" in response.text
    assert "Accept_Block" in response.text
    assert "Start" in response.text
    assert "second_player" in response.text


def test_websocket_connect(client):
    with client.websocket_connect("/ws/1") as websocket:
        data = {"message_txt": "Start"}
        websocket.send_text(json.dumps(data))
        response = websocket.receive_text()
        assert "alert" in response

        data = {"message_txt": "Take 3 coins"}
        websocket.send_text(json.dumps(data))
        response = websocket.receive_text()
        assert "alert" in response
