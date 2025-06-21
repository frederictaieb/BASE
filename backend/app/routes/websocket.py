from fastapi import WebSocket, WebSocketDisconnect
from app.models.client import Client
from typing import List

clients: List[Client] = []

async def websocket_endpoint(websocket: WebSocket, username: str):
    await websocket.accept()
    client = Client(username=username, websocket=websocket)
    clients.append(client)

    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Hello {username}, you said: {data}")
    except WebSocketDisconnect:
        clients.remove(client)