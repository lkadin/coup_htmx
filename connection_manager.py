from fastapi import WebSocket
from content import Content
from coup import Game


class ConnectionManager:
    def __init__(self, game: Game) -> None:
        self.active_connections = {}
        self.game = game

    async def connect(self, user_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    async def disconnect(self, user_id: str, websocket: WebSocket):
        del self.active_connections[user_id]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, game: Game, message_type: str = "all"):
        for user_id, websocket in self.active_connections.items():
            game.user_id = user_id
            content = Content(game, user_id)

            if message_type in ("all", "alert"):
                table = content.show_game_alert()
                await self.send_personal_message(table, websocket)
                table = content.show_player_alert(user_id)
                await self.send_personal_message(table, websocket)

            if message_type in ("all", "history"):
                history = content.show_history()
                await self.send_personal_message(history, websocket)

            if message_type in ("all", "table"):
                table = content.show_table()
                await self.send_personal_message(
                    table,
                    websocket,
                )

            if message_type in ("all", "turn"):
                table = content.show_turn()
                await self.send_personal_message(
                    table,
                    websocket,
                )

            # if message_type in ("all", "game_status"):
            #     table = content.show_game_status()
            #     await self.send_personal_message(table, websocket)

            if message_type in ("all", "action"):
                table = content.show_actions()
                await self.send_personal_message(table, websocket)

            if message_type in ("pick") and self.game.your_turn():
                table = content.pick_second_player()
                await self.send_personal_message(table, websocket)

            if message_type in ("hide") and self.game.your_turn():
                table = content.hide_second_player()
                await self.send_personal_message(table, websocket)
