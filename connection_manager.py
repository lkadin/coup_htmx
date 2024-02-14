from fastapi import WebSocket
from datetime import datetime
from content import Content
from coup import Game


class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: list[str, WebSocket] = {}

    async def connect(self, user_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    async def disconnect(self, user_id: str, websocket: WebSocket):
        del self.active_connections[user_id]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, game: Game):
        time = datetime.now()
        for user_id, websocket in self.active_connections.items():
            content = f"""
            <div hx-swap-oob="beforeend:#notifications">
            <p>{time}: {message}</p>
            </div>
            """
            await self.send_personal_message(content, websocket)

            html = Content(game,user_id)
            content = html.html()
            await self.send_personal_message(content, self.active_connections[user_id])
