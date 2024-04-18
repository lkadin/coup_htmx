import json
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_read_item():
    response = client.get("/web/1/")
    assert response.status_code == 200
    assert "Lee" in response.text


def test_websocket_chat():
    with client.websocket_connect("/ws/1") as websocket:
        data = {"message_txt": "Test message"}
        websocket.send_text(json.dumps(data))
        response = websocket.receive_text()
        assert "#history" in response
