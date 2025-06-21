from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from app.routes import api
from app.routes import websocket as ws_route

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure les routes HTTP sous le préfixe "/eaim/fastapi"
app.include_router(api.router)

# Ajouter la route WebSocket manuellement (sans le routeur)
@app.websocket("/ws/{username}")
async def websocket_entrypoint(websocket: WebSocket, username: str):
    await ws_route.websocket_endpoint(websocket, username)