from fastapi import FastAPI, WebSocket, Request
import json
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn
from connection_manager import ConnectionManager
from coup import Game

# from content import Content

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
    game.wait()
    await manager.broadcast(
        f" {game.players[user_id].name} has joined ", game, "notification"
    )

    while game.status == "Waiting":
        data = await websocket.receive_text()
        message = json.loads(data)
        await process_message(websocket, user_id, message)


async def process_message(websocket, user_id, message):
    print(message["message_txt"])
    if not game.your_turn(user_id):
        # content = Content(game, user_id).not_your_turn(True)
        # await manager.send_personal_message(content, websocket)
        return

    if message["message_txt"] == "Start":
        game.start()

    game.next_turn()
    await clear_and_show_board(websocket, user_id, message)


async def clear_and_show_board(websocket, user_id, message):
    # content = Content(game, user_id).not_your_turn(False)
    # await manager.send_personal_message(content, websocket)
    await manager.broadcast(
        f" {game.players[user_id].name} says: {message['message_txt']}",
        game,
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
