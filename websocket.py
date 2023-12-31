from fastapi import FastAPI, WebSocket
import json

app = FastAPI()

# List to store connected WebSocket clients
connected_clients = []


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # Connect client
    await websocket.accept()
    connected_clients.append(websocket)

    try:
        while True:
            # Receive message from the client
            data = await websocket.receive_text()
            print(data)

            # Broadcast the message to all connected clients
            for client in connected_clients:
                print(client)
                # await client.send_text(f"User {id(websocket)} says: {data}")
                jdata = json.dumps({"Name": "Lee"})
                await client.send_json(jdata, mode="text")
                print("I sent it")

    except Exception as e:
        print(f"WebSocket Error: {e}")

    finally:
        # Disconnect client
        connected_clients.remove(websocket)
        await websocket.close()
