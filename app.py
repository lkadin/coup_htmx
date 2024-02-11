from fastapi import FastAPI, WebSocket, Request
import json
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn
from connection_manager import ConnectionManager

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")





manager = ConnectionManager()


@app.get("/web/{room_id}/", response_class=HTMLResponse)
async def read_itemx(request: Request, room_id: str):
    return templates.TemplateResponse(
        "htmx_client_generic.html",
        {"request": request, "room_id": room_id},
    )


@app.websocket("/ws/{room_id}")
async def websocket_chat(websocket: WebSocket, room_id: str):
    await manager.connect(room_id, websocket)
    print(f"room-{room_id}")
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            print(f"{message=}")
            await manager.broadcast(
                f" {message['user_name']} in room {room_id} says: {message['message_txt']}",
                websocket,
            )
    except Exception as e:
        print("Got an exception ", e)
        await manager.disconnect(room_id, websocket)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
