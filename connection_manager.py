from fastapi import FastAPI, WebSocket, Request
import json
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, PlainTextResponse
import uvicorn

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

    async def broadcast(self, message: str, room_id: str, websocket: WebSocket):
        for room, websocket in self.active_connections.items():
            print(room, websocket)
            await websocket[0].send_text(message)
        await self.send_personal_message(
            "This goes to 2 only", self.active_connections["2"][0]
        )


manager = ConnectionManager()


@app.get("/web1/", response_class=HTMLResponse)
async def read_item1(request: Request):
    return templates.TemplateResponse(
        "web_client_1.html",
        {
            "request": request,
        },
    )


@app.get("/web2/", response_class=HTMLResponse)
async def read_item2(request: Request):
    return templates.TemplateResponse(
        "web_client_2.html",
        {
            "request": request,
        },
    )


@app.get("/web3/", response_class=HTMLResponse)
async def read_item3(request: Request):
    return templates.TemplateResponse(
        "web_client_3.html",
        {
            "request": request,
        },
    )


@app.get("/web4/", response_class=HTMLResponse)
async def read_item4(request: Request):
    return templates.TemplateResponse(
        "web_client_4.html",
        {
            "request": request,
        },
    )


@app.get("/htmx/", response_class=PlainTextResponse)
async def read_htmx(request: Request):
    return "<h1>This is the response</h1>" 

@app.get("/joke/", response_class=HTMLResponse)
async def joke(request: Request):
    return templates.TemplateResponse(
        "joke.html",
        {
            "request": request,
        },
    )


@app.websocket("/ws/{room_id}")
async def websocket_chat(websocket: WebSocket, room_id: str):
    await manager.connect(room_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"{data=}")
            message = json.loads(data)
            print(f"{message=}")
            await manager.broadcast(
                f" {message['user_name']} in room {room_id} says: {message['message_txt']}",
                room_id,
                websocket,
            )
    except Exception as e:
        print("Got an exception ", e)
        await manager.disconnect(room_id, websocket)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
