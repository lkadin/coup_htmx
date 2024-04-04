from fastapi import FastAPI, WebSocket, Request
import json
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn
from connection_manager import ConnectionManager
from coup import Game


app = FastAPI()

templates = Jinja2Templates(directory="templates")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# ids = [("1", "Lee"), ("2", "Adina"), ("3", "Joey"), ("9", "Jamie")]
ids = [("1", "Lee"), ("2", "Adina")]
game = Game()
manager = ConnectionManager(game)
game.add_all_players(ids)
game.wait()


@app.get("/web/{user_id}/", response_class=HTMLResponse)
async def read_item(request: Request, user_id: str):
    user_name = game.players[user_id].name
    return templates.TemplateResponse(
        "htmx_user_generic.html",
        {
            "request": request,
            "user_id": user_id,
            "user_name": user_name,
            "actions": game.actions,
            "game_status": game.game_status,
            "turn": game.whose_turn_name(),
        },
    )


@app.websocket("/ws/{user_id}")
async def websocket_chat(websocket: WebSocket, user_id: str):
    await manager.connect(user_id, websocket)
    await manager.broadcast(
        f" {game.players[user_id].name} has joined ", game, "notification"
    )
    try:
        while True:
            data = await websocket.receive_text()
            if data:
                message = json.loads(data)
                await process_message(websocket, user_id, message)

    except Exception as e:
        message = f"{game.players[user_id].name} has disconnected"
        await manager.disconnect(user_id, websocket)
        await manager.broadcast(message, game)
        print(f"Exception = {e}")


async def process_message(websocket, user_id, message):

    if message.get("message_txt"):
        game.set_current_action(
            game.action_from_action_name(message.get("message_txt"))
        )
    else:
        message["message_txt"] = game.current_action

    game.set_second_player(game.player_id(message.get("player")))
    game.cards_to_exchange = message.get("cardnames")

    if game.current_action.second_player_required:
        await manager.broadcast(
            f" {game.players[user_id].name}: {message['message_txt']}",
            game,
            message_type="pick",
        )

    if game.second_player:
        await manager.broadcast(
            f" {game.players[user_id].name}: {message['message_txt']}",
            game,
            message_type="hide",
        )
    if message.get("message_txt") == "Exchange" and not game.cards_to_exchange:
        game.process_action(message["message_txt"], user_id)
        await manager.broadcast(
            f" {game.players[user_id].name}: {message['message_txt']}",
            game,
            message_type="exchange_draw",
        )

    game.process_action(message["message_txt"], user_id)
    await manager.broadcast(
        f" {game.players[user_id].name}: {message['message_txt']}",
        game,
    )
    if not game.exchange_in_progress:
        await manager.broadcast(
            f" {game.players[user_id].name}: {message['message_txt']}",
            game,
            message_type="hide_exchange",
        )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
