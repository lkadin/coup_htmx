import asyncio
import websockets
import json

USER_NAME = "Client 4"


async def test():
    message = {"user_name": USER_NAME, "message_txt": "This is my message"}
    json_message = json.dumps(message)
    async with websockets.connect("ws://localhost:8000/ws/4") as websocket:
        while True:
            message = input("enter Message   ")
            new_message = {"user_name": USER_NAME, "message_txt": message}
            json_message = json.dumps(new_message)
            await websocket.send(json_message)
            response = await websocket.recv()
            print(response)


asyncio.get_event_loop().run_until_complete(test())
