from fastapi import FastAPI, WebSocket
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import json

templates = Jinja2Templates(directory="templates")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: list[str, WebSocket] = {}
        print("Creating a list to hold active connections", self.active_connections)

    async def connect(self, room_id: str, websocket: WebSocket):
        await websocket.accept()
        if not self.active_connections.get(room_id):
            self.active_connections[room_id] = []
        self.active_connections[room_id].append(websocket)

    async def disconnect(self, room_id: str, websocket: WebSocket):
        self.active_connections[room_id].remove(websocket)
        print("After disconnect active connections are: ", self.active_connections)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
        print("Sent a personal msg to , ", websocket)

    async def broadcast(self, message: str, room_id: str, websocket: WebSocket):
            for room,websocket in self.active_connections.items():
                print(room,websocket[0])
                await websocket[0].send_text(message)
            # for connection in self.active_connections[user_name]:
                # print(connection)
                # await connection.send_text(message)
                # print(f"In broadcast: sent {message} to ", room_id, connection.client)


manager = ConnectionManager()


@app.websocket("/ws/{room_id}")
async def websocket_chat(websocket: WebSocket, room_id: str):
    await manager.connect(room_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            print(message)
            await manager.broadcast(
                f" {message['user_name']} in room {room_id} says: {message['message_txt']}",
                room_id,
                websocket,
            )
    except Exception as e:
        print("Got an exception ", e)
        await manager.disconnect(room_id, websocket)
