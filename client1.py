import asyncio
import websockets
import json


async def test():
    message={"user_name":"Lee","message_txt":"This is my message"}
    json_message=json.dumps(message)
    print(f"string - {json_message}")
    async with websockets.connect(
        "ws://localhost:8000/ws/1"
    ) as websocket:
        await websocket.send(json_message)
        response = await websocket.recv()
        print(response)
        response = await websocket.recv()
        print(response)


asyncio.get_event_loop().run_until_complete(test())
