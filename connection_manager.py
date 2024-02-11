from fastapi import WebSocket
from datetime import datetime
from content import Content
from coup import Game


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

    async def broadcast(self, message: str, websocket: WebSocket, game: Game):
        time = datetime.now()
        content = f"""
            <div hx-swap-oob="beforeend:#notifications">
            <p>{time}: {message}</p>
            </div>
        """
        for room, websocket in self.active_connections.items():
            await self.send_personal_message(content, self.active_connections[room][0])
        content = f"""
            <div hx-swap-oob="beforeend:#private_message">
            <p>{time}: PRIVATE</p>
            </div>
        """
        await self.send_personal_message(content, self.active_connections["1"][0])

        content = """
            <div hx-swap-oob="innerHTML:#photo">
            <img src="/static/jpg/duke.JPG" alt="duke">
            </div>
        """
        await self.send_personal_message(content, self.active_connections["3"][0])

        html = Content("1")
        content = html.html()
        await self.send_personal_message(content, self.active_connections["2"][0])
