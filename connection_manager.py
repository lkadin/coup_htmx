from fastapi import WebSocket
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
        for user_id, websocket in self.active_connections.items():
            content = f"""
            <div hx-swap-oob="beforeend:#notifications">
            <p>{message}</p>
            </div>
            """
            await self.send_personal_message(content, websocket)

            content = Content(game, user_id)
            table = content.show_table()
            await self.send_personal_message(table, self.active_connections[user_id])

            turn = content.whose_turn()
            await self.send_personal_message(turn, self.active_connections[user_id])

            not_you_turn = content.not_your_turn(False)
            await self.send_personal_message(
                not_you_turn, self.active_connections[user_id]
            )
