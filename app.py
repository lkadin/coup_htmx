from fastapi import FastAPI, WebSocket, Request
import json
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn
from connection_manager import ConnectionManager
from coup import Game
from content import Content

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

ids = [("1", "Lee"), ("2", "Adina"), ("3", "Joey"), ("9", "Jamie")]
game = Game(ids)
# game.play()
game.players["1"].add_remove_coins(4)
game.players["9"].add_remove_coins(-1)
manager = ConnectionManager()


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
        },
    )


@app.websocket("/ws/{user_id}")
async def websocket_chat(websocket: WebSocket, user_id: str):
    await manager.connect(user_id, websocket)
    print(game.status)
    if game.status == "Not started":
        await manager.broadcast(
            "Start of game",
            game,
        )
        game.play()
        print(game.status)

    # try:
    while game.status == "In progress":
        data = await websocket.receive_text()
        message = json.loads(data)
        if game.whose_turn_name() != game.players[user_id].name:
            content = Content(game, user_id).not_your_turn(True)
            await manager.send_personal_message(content, websocket)
        else:
            game.next_turn()
            content = Content(game, user_id).not_your_turn(False)
            await manager.send_personal_message(content, websocket)
            await manager.broadcast(
                f" {game.players[user_id].name} says: {message['message_txt']}",
                game,
            )
    # except Exception as e:
    #     print("Got an exception ", e)
    # await manager.disconnect(user_id, websocket)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
