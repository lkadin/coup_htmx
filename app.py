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

MAXPLAYERS = 4
game = Game()
manager = ConnectionManager(game)
game.wait()


@app.get("/", response_class=HTMLResponse)
async def login(request: Request):
    if len(game.players) >= MAXPLAYERS:
        return templates.TemplateResponse("no_more_players.html", {"request": request})
    if game.game_status != "Waiting":
        return templates.TemplateResponse("game_started.html", {"request": request})

    user_id = len(game.players) + 1
    return templates.TemplateResponse(
        "login.html", {"request": request, "user_id": user_id}
    )


@app.get("/web/{user_id}/", response_class=HTMLResponse)
async def read_item(request: Request, user_id: str, user_name: str):
    def refresh():
        if already_logged_in(user_id) and already_in_game(user_name):
            return True

    def already_in_game(user_name):
        for player in game.player_ids:
            if player[1] == user_name:
                return True

    def already_logged_in(user_id):  # websocket (user_id) already in use
        if manager.active_connections.get(user_id):
            return True

    def game_started():
        if game.game_status != "Waiting":
            return True

    if refresh():
        print("refresh")
        return templates.TemplateResponse(
            "htmx_user_generic.html",
            {
                "request": request,
                "user_id": user_id,
                "user_name": user_name,
                "actions": game.actions,
                "game_status": game.game_status,
                "turn": game.whose_turn_name(),
                "history": game.action_history,
            },
        )

    if already_logged_in(user_id):
        return templates.TemplateResponse(
            "id_already_in_game.html",
            {
                "request": request,
            },
        )

    if already_in_game(user_name):
        return templates.TemplateResponse(
            "player_already_in_game.html", {"request": request}
        )

    if game_started():
        return templates.TemplateResponse(
            "game_started.html",
            {
                "request": request,
            },
        )

    game.add_player(user_id, user_name)  # Try to add the player to the game
    return templates.TemplateResponse(
        "htmx_user_generic.html",
        {
            "request": request,
            "user_id": user_id,
            "user_name": user_name,
            "actions": game.actions,
            "game_status": game.game_status,
            "turn": game.whose_turn_name(),
            "history": game.action_history,
        },
    )


@app.websocket("/ws/{user_id}")
async def websocket_chat(websocket: WebSocket, user_id: str):
    await manager.connect(user_id, websocket)
    await manager.broadcast(
        # f" {game.players[user_id].name} has joined ", game, "history"
        f" {user_id} has joined ",
        game,
        "history",
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
        game.set_current_action(message.get("message_txt"), user_id)
    else:
        message["message_txt"] = game.current_action

    game.set_second_player(game.player_id(message.get("player")))

    if game.exchange_in_progress:
        game.cards_to_exchange = message.get("cardnames")

    if game.coup_in_progress:
        game.card_to_lose = message.get("cardnames")

    if game.assassinate_in_progress:
        game.card_to_lose = message.get("cardnames")

    if game.current_action.second_player_required and not game.second_player:
        await manager.broadcast(
            f" {game.players[user_id].name}: {message['message_txt']}",
            game,
            message_type="pick",
        )

    if game.second_player or game.coup_in_progress or game.assassinate_in_progress:
        await manager.broadcast(
            f" {game.players[user_id].name}: {message['message_txt']}",
            game,
            message_type="hide",
        )

    game.check_coins(user_id)  # set player alert if necessary
    game.process_action(message["message_txt"], user_id)
    await manager.broadcast(
        f" {game.players[user_id].name}: {message['message_txt']}",
        game,
    )


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
