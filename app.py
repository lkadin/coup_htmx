from fastapi import FastAPI, WebSocket, Request, WebSocketDisconnect
import json
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn
from connection_manager import ConnectionManager
from coup import Game, Action
import traceback

templates = Jinja2Templates(directory="templates")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

MAXPLAYERS = 4


def setup_game():
    game = Game()
    manager = ConnectionManager(game)
    game.wait()
    return game, manager


game, manager = setup_game()


@app.get("/", response_class=HTMLResponse)
async def login(request: Request):
    if len(game.players) >= MAXPLAYERS:
        return templates.TemplateResponse("no_more_players.html", {"request": request})
    if game.game_status != "Waiting":
        return templates.TemplateResponse("game_started.html", {"request": request})

    user_id = game.next_user_id()
    return templates.TemplateResponse(
        "login.html", {"request": request, "user_id": user_id}
    )


@app.get("/reset", response_class=HTMLResponse)
async def reset(request: Request):
    user_id = game.next_user_id()
    game.reset()
    manager.active_connections = {}
    game.wait()
    return templates.TemplateResponse(
        "reset.html", {"request": request, "user_id": user_id}
    )


@app.get("/restart", response_class=HTMLResponse)
async def restart(request: Request):
    game.restart()
    return templates.TemplateResponse(
        "restart.html",
        {
            "request": request,
        },
    )


@app.get("/hidden_checkbox", response_class=HTMLResponse)
async def hidden_checkbox(request: Request):
    return templates.TemplateResponse("hidden_checkbox.html", {"request": request})


@app.get("/web/{user_id}/{action}", response_class=HTMLResponse)
async def get_action(request: Request, user_id: str, action: str):
    print(user_id, action)
    message = {"message_txt": action}
    await process_message(user_id, message)  # type: ignore
    # await bc(user_id, message)


@app.get("/web/{user_id}/", response_class=HTMLResponse)
async def read_item(request: Request, user_id: str, user_name: str):
    def refresh():
        if game.players.get(user_id):
            if game.players[user_id].name == user_name:
                return True

    def already_in_game(
        user_id, user_name
    ):  # if user is logged in with a different ID return True
        for player in game.players:
            if (game.players[player].name) == user_name and game.players[
                player
            ].id != user_id:
                return True

    def already_logged_in(user_id, user_name):  # websocket (user_id) already in use
        if manager.active_connections.get(user_id) and not already_in_game(
            user_id, user_name
        ):
            return True

    def game_started():
        if game.game_status != "Waiting":
            return True

    if refresh():
        print("refresh")
        await bc(user_id, message={"message_txt": ""})

    elif already_logged_in(user_id, user_name):
        return templates.TemplateResponse(
            "id_already_in_game.html",
            {
                "request": request,
            },
        )

    elif already_in_game(user_id, user_name):
        return templates.TemplateResponse(
            "player_already_in_game.html", {"request": request}
        )

    elif game_started():
        return templates.TemplateResponse(
            "game_started.html",
            {
                "request": request,
            },
        )

    game.add_player(user_id, user_name)  # Try to add the player to the game
    history = game.action_history
    if not history:
        history = ""
    game.prep_history_list()
    return templates.TemplateResponse(
        "htmx_user_generic.html",
        {
            "request": request,
            "user_id": user_id,
            "user_name": user_name,
            "actions": game.actions,
            "game_status": game.game_status,
            "turn": game.whose_turn_name(),
            "suffix": game.get_suffix(),
            "history_list": game.history_list,
            "player_names": [],
            "second_player_visible": "hidden",
        },
    )


async def bc(user_id, message, message_type="all"):
    await manager.broadcast(
        f" {game.players[user_id].name}: {message['message_txt']}",
        game,
        message_type,
    )


@app.websocket("/ws/{user_id}")
async def websocket_chat(websocket: WebSocket, user_id: str):
    await manager.connect(user_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            if data:
                message = json.loads(data)
                await process_message(user_id, message)  # type: ignore

    except WebSocketDisconnect as e:
        if e.code == 1001:  # type: ignore
            message = f"{user_id} has disconnected"
            print(f"{user_id} has disconnected")
            await manager.disconnect(user_id, websocket)
            await manager.broadcast(message, game)
        else:
            print(f"Exception = {e}")
            print(traceback.format_exc())


async def process_message(user_id, message):

    if message.get("message_txt") and not game.exchange_in_progress:
        game.set_current_action(message.get("message_txt"), user_id)
    else:
        message["message_txt"] = ""

    game.set_second_player_id(game.player_id(message.get("player")))
    if game.current_action.name in ("Steal", "Assassinate", "Exchange", "Coup"):
        message["message_txt"] = game.current_action

    if game.exchange_in_progress:
        game.cards_to_exchange = message.get("cardnames")
        if isinstance(game.cards_to_exchange, str):
            game.cards_to_exchange = [game.cards_to_exchange]

    if game.lose_influence_in_progress and not game.current_action.name == "Block":
        game.card_name_to_lose = message.get("cardnames")
        message["message_text"] = (
            ""  # just getting cards to lose - no other action necessary
        )

    if (
        game.current_action.second_player_required
        and not game.second_player_id
        and game.player_index_to_id(game.whose_turn()) == game.players[game.user_id].id
        and not game.block_in_progress
    ):
        await bc(user_id, message, "pick")

    if game.second_player_id or game.coup_assassinate_in_progress:
        await bc(user_id, message, "hide")

    game.check_coins(user_id)  # set player alert if necessary
    game.process_action(message["message_txt"], user_id)
    await bc(user_id, message)
    if game.game_over():
        game.process_action(Action("No_action", 0, "disabled", False), user_id)
        await bc(user_id, message)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
