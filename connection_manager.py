from fastapi import WebSocket
from datetime import datetime
from content import Content
from coup import Game


class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: list[str, WebSocket] = {}

    async def connect(self, user_id: str, websocket: WebSocket):
        await websocket.accept()
        if not self.active_connections.get(user_id):
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)

    async def disconnect(self, user_id: str, websocket: WebSocket):
        self.active_connections[user_id].remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, game: Game, user_id: str):
        time = datetime.now()
        content = f"""
            <div hx-swap-oob="beforeend:#notifications">
            <p>{time}: {message}</p>
            </div>
        """
        for user_id, websocket in self.active_connections.items():
            await self.send_personal_message(
                content, self.active_connections[user_id][0]
            )
        content = f"""
            <div hx-swap-oob="beforeend:#private_message">
            <p>{time}: PRIVATE</p>
            </div>
        """
        await self.send_personal_message(content, self.active_connections["1"][0])

        html = Content(game.player_ids, "3")
        content = html.html()
        await self.send_personal_message(content, self.active_connections["3"][0])

        html = Content(game.player_ids, "2")
        content = html.html()
        await self.send_personal_message(content, self.active_connections["2"][0])

        html = Content(game.player_ids, "9")
        content = html.html()
        await self.send_personal_message(content, self.active_connections["9"][0])
