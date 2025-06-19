from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from app.models.client import Client
from typing import List

app = FastAPI()
clients: List[Client] = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/helloworld")
async def helloworld():
    return {"message": "Hello from FastAPI!"}

@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await websocket.accept()
    client = Client(username=username, websocket=websocket)
    clients.append(client)

    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Hello {client.username}, you said: {data}")
    except WebSocketDisconnect:
        clients.remove(client)

