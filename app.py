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

game = Game(["1", "2", "3", "9"])
game.play()
manager = ConnectionManager()


@app.get("/web/{user_id}/", response_class=HTMLResponse)
async def read_itemx(request: Request, user_id: str):
    return templates.TemplateResponse(
        "htmx_user_generic.html",
        {"request": request, "user_id": user_id},
    )


@app.websocket("/ws/{user_id}")
async def websocket_chat(websocket: WebSocket, user_id: str):
    await manager.connect(user_id, websocket)
    print(f"room-{user_id}")
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            # print(f"{message=}")
            await manager.broadcast(
                f" {message['user_name']} in room {user_id} says: {message['message_txt']}",
                websocket,
                game,user_id
            )
    except Exception as e:
        print("Got an exception ", e)
        await manager.disconnect(user_id, websocket)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
