from fastapi import FastAPI, WebSocket, Request
import json
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn
from datetime import datetime

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: list[str, WebSocket] = {}
        print("Creating a list to hold active connections", self.active_connections)

    async def connect(self, room_id: str, websocket: WebSocket):
        await websocket.accept()
        if not self.active_connections.get(room_id):
            self.active_connections[room_id] = []
        self.active_connections[room_id].append(websocket)

    async def disconnect(self, room_id: str, websocket: WebSocket):
        self.active_connections[room_id].remove(websocket)
        print("After disconnect active connections are: ", self.active_connections)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
        print("Sent a personal msg to , ", websocket)

    async def broadcast(self, message: str,  websocket: WebSocket):
        time = datetime.now()
        content = f"""
            <div hx-swap-oob="beforeend:#notifications">
            <p>{time}: {message}</p>
            </div>
        """
        for room, websocket in self.active_connections.items():
            await self.send_personal_message(content, self.active_connections[room][0])
        # await self.send_personal_message(content, self.active_connections["2"][0])

        # await self.send_personal_message(content, self.active_connections["3"][0])


manager = ConnectionManager()


@app.get("/web/{room_id}/", response_class=HTMLResponse)
async def read_itemx(request: Request, room_id: str):
    return templates.TemplateResponse(
        f"htmx_client_{room_id}.html",
        {
            "request": request,
        },
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
                # room_id,
                websocket,
            )
    except Exception as e:
        print("Got an exception ", e)
        await manager.disconnect(room_id, websocket)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
