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
async def read_itemx(request: Request, user_id: str):
    user_name = game.players[user_id].name
    return templates.TemplateResponse(
        "htmx_user_generic.html",
        {
            "request": request,
            "user_id": user_id,
            "user_name": user_name,
            "actions": game.actions,
            "status": game.status,
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
        message = f"{game.players[user_id].name} has disconnetd"
        await manager.disconnect(user_id, websocket)
        await manager.broadcast(message, game)
        print(e)


async def process_message(websocket, user_id, message):

    def second_player():
        if not message.get("message_txt"):
            message["message_txt"] = "Not Sent"
        try:
            game.second_player = game.player_id(message["player"])
            game.steal(give_to=user_id, steal_from=game.second_player)
        except KeyError:
            game.second_player = None

    second_player()  # check if second player was passed

    if message["message_txt"] in ("Assassinate", "Coup", "Steal"):
        await manager.broadcast(
            f" {game.players[user_id].name} says: {message['message_txt']}",
            game,
            message_type="pick",
        )

    # if not game.second_player:
    #     await manager.broadcast(
    #         f" {game.players[user_id].name} says: {message['message_txt']}",
    #         game,
    #         message_type="hide",
    #     )

    game.process_action(message["message_txt"], user_id)
    await manager.broadcast(
        f" {game.players[user_id].name} says: {message['message_txt']}",
        game,
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
